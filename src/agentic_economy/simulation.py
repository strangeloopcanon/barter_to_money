"""Simulation engine for barter vs money/Exchange agent interactions."""

from __future__ import annotations

import json
import logging
import random
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from . import prompts
from .llm_client import LLMClient

logger = logging.getLogger(__name__)


@dataclass
class MessageLogEntry:
    round_number: int
    sender: str
    receiver: str
    message_id: str
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "round": self.round_number,
            "sender": self.sender,
            "receiver": self.receiver,
            "message_id": self.message_id,
            "payload": self.payload,
        }


@dataclass
class AgentState:
    name: str
    inventory: Dict[str, int]
    target_good: str
    money: float = 0.0
    history: List[Dict[str, Any]] = field(default_factory=list)

    def recent_history(self, history_limit: int) -> List[Dict[str, Any]]:
        return self.history[-history_limit:]


@dataclass
class SimulationResult:
    condition: str
    n_agents: int
    seed: int
    rounds_run: int
    messages: List[MessageLogEntry]
    agents: Dict[str, Dict[str, str]]
    inventory_final: Dict[str, Dict[str, int]]
    successful_agents: int
    parameters: Dict[str, Any]
    exchange_inventory: Optional[Dict[str, int]] = None
    exchange_money: Optional[float] = None
    exchange_price_history: Optional[List[Dict[str, float]]] = None
    exchange_round_metrics: Optional[List[Dict[str, Any]]] = None
    events: Optional[List[Dict[str, Any]]] = None
    behavior_summary: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "condition": self.condition,
            "N": self.n_agents,
            "seed": self.seed,
            "rounds_run": self.rounds_run,
            "agents": self.agents,
            "messages": [entry.to_dict() for entry in self.messages],
            "inventory_final": self.inventory_final,
            "successful_agents": self.successful_agents,
            "parameters": self.parameters,
            "exchange_inventory": self.exchange_inventory,
            "exchange_money": self.exchange_money,
            "exchange_price_history": self.exchange_price_history,
            "exchange_round_metrics": self.exchange_round_metrics,
            "events": self.events,
            "behavior_summary": self.behavior_summary,
        }

    def write_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(self.to_dict(), handle, indent=2, ensure_ascii=True)


class BaseSimulation:
    def __init__(
        self,
        n_agents: int,
        rounds: int,
        seed: int,
        history_limit: int,
        llm_client: LLMClient,
        model_name: str,
    ):
        self.n_agents = n_agents
        self.rounds = rounds
        self.random = random.Random(seed)  # nosec B311 - deterministic simulation RNG
        self.history_limit = history_limit
        self.llm_client = llm_client
        self.model_name = model_name

        self.goods = [f"g{i}" for i in range(n_agents)]
        self.agents: Dict[str, AgentState] = {}
        self.messages: List[MessageLogEntry] = []
        self._proposals: Dict[str, MessageLogEntry] = {}
        self._message_counter = 0
        self._seed = seed
        self.events: List[Dict[str, Any]] = []

    def _next_message_id(self) -> str:
        message_id = f"m{self._message_counter}"
        self._message_counter += 1
        return message_id

    def _log_event(self, event: str, **fields: Any) -> None:
        record = {"event": event, **fields}
        self.events.append(record)

    def _log_agent_action(
        self, round_number: int, agent_state: AgentState, action: Mapping[str, Any]
    ) -> None:
        self._log_event(
            "agent_action",
            round=round_number,
            agent=agent_state.name,
            action=dict(action),
            inventory=dict(agent_state.inventory),
            target_good=agent_state.target_good,
            money=agent_state.money,
        )

    def _behavior_summary(self) -> Dict[str, Any]:
        summary: Dict[str, Any] = {}
        for agent_name in self.agents:
            proposals = [
                msg
                for msg in self.messages
                if msg.sender == agent_name and msg.payload.get("action") == "propose_trade"
            ]
            proposal_terms = [
                (
                    msg.payload.get("to"),
                    msg.payload.get("give"),
                    msg.payload.get("receive"),
                )
                for msg in proposals
            ]
            unique_partners = len({term[0] for term in proposal_terms if term[0]})
            repeated_identical = len(proposal_terms) - len(set(proposal_terms))
            send_messages = [
                msg
                for msg in self.messages
                if msg.sender == agent_name and msg.payload.get("action") == "send_message"
            ]
            invalid_actions = [
                ev
                for ev in self.events
                if ev.get("event") == "invalid_action" and ev.get("agent") == agent_name
            ]
            summary[agent_name] = {
                "proposals": len(proposals),
                "unique_partners": unique_partners,
                "repeated_identical_proposals": repeated_identical,
                "messages_sent": len(send_messages),
                "invalid_actions": len(invalid_actions),
            }
        return summary

    def _record_history(self, agent_name: str, direction: str, message: MessageLogEntry) -> None:
        entry = {
            "direction": direction,
            "from": message.sender,
            "to": message.receiver,
            "message_id": message.message_id,
            "round": message.round_number,
            "payload": message.payload,
        }
        state = self.agents[agent_name]
        state.history.append(entry)
        # Trim history to keep prompt sizes bounded.
        if len(state.history) > self.history_limit:
            state.history = state.history[-self.history_limit :]

    def _log_message(self, message: MessageLogEntry) -> None:
        self.messages.append(message)
        if message.sender in self.agents:
            self._record_history(message.sender, "outgoing", message)
        if message.receiver in self.agents:
            self._record_history(message.receiver, "incoming", message)

    def _inventory_snapshot(self) -> Dict[str, Dict[str, int]]:
        return {name: dict(state.inventory) for name, state in self.agents.items()}

    def _agent_metadata(self) -> Dict[str, Dict[str, str]]:
        return {
            name: {"endowment": next(iter(state.inventory.keys())), "target": state.target_good}
            for name, state in self.agents.items()
        }

    def _success_count(self) -> int:
        count = 0
        for state in self.agents.values():
            if state.inventory.get(state.target_good, 0) >= 1:
                count += 1
        return count

    def _derangement(self) -> List[int]:
        if self.n_agents == 1:
            return [0]
        indices = list(range(self.n_agents))
        while True:
            self.random.shuffle(indices)
            if all(idx != target for idx, target in enumerate(indices)):
                return indices


class BarterSimulation(BaseSimulation):
    def __init__(
        self,
        n_agents: int,
        rounds: int,
        seed: int,
        history_limit: int,
        llm_client: LLMClient,
        model_name: str,
    ):
        super().__init__(n_agents, rounds, seed, history_limit, llm_client, model_name)
        target_indices = self._derangement()
        for idx in range(n_agents):
            agent_name = f"A{idx}"
            endowment = self.goods[idx]
            target = self.goods[target_indices[idx]]
            self.agents[agent_name] = AgentState(
                name=agent_name, inventory={endowment: 1}, target_good=target
            )

    def run(self) -> SimulationResult:
        for round_number in range(1, self.rounds + 1):
            actions: Dict[str, Dict[str, Any]] = {}
            for agent in self.agents.values():
                system_prompt = prompts.barter_system_prompt(
                    agent.name, agent.inventory, agent.target_good
                )
                user_prompt = prompts.barter_user_prompt(
                    round_number,
                    agent.recent_history(self.history_limit),
                    agent.inventory,
                    agent.target_good,
                )
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
                action = self.llm_client.complete_json(messages)
                self._log_agent_action(round_number, agent, action)
                actions[agent.name] = action

            self._apply_barter_actions(actions, round_number)
            if self._success_count() == self.n_agents:
                break

        return SimulationResult(
            condition="barter",
            n_agents=self.n_agents,
            seed=self._seed,
            rounds_run=round_number,
            messages=self.messages,
            agents=self._agent_metadata(),
            inventory_final=self._inventory_snapshot(),
            successful_agents=self._success_count(),
            parameters={
                "rounds": self.rounds,
                "history_limit": self.history_limit,
                "model": self.model_name,
            },
            events=self.events,
            behavior_summary=self._behavior_summary(),
        )

    def _apply_barter_actions(
        self, actions: Mapping[str, Dict[str, Any]], round_number: int
    ) -> None:
        for sender, action in actions.items():
            action_name = action.get("action")
            if action_name == "send_message":
                receiver = action.get("to")
                message_text = action.get("message")
                if (
                    not receiver
                    or receiver not in self.agents
                    or receiver == sender
                    or not isinstance(message_text, str)
                    or not message_text.strip()
                ):
                    self._log_event(
                        "invalid_action",
                        round=round_number,
                        agent=sender,
                        reason="invalid_send_message",
                        action=action,
                    )
                    continue
                message_id = self._next_message_id()
                message = MessageLogEntry(
                    round_number=round_number,
                    sender=sender,
                    receiver=receiver,
                    message_id=message_id,
                    payload=action,
                )
                self._log_message(message)
                self._log_event(
                    "message_sent",
                    round=round_number,
                    sender=sender,
                    receiver=receiver,
                    message_id=message_id,
                )
                continue
            if action_name == "propose_trade":
                receiver = action.get("to")
                give_good = action.get("give")
                receive_good = action.get("receive")
                if not receiver or receiver not in self.agents:
                    self._log_event(
                        "invalid_action",
                        round=round_number,
                        agent=sender,
                        reason="invalid_receiver",
                        action=action,
                    )
                    continue
                if not give_good or not receive_good:
                    self._log_event(
                        "invalid_action",
                        round=round_number,
                        agent=sender,
                        reason="missing_trade_fields",
                        action=action,
                    )
                    continue
                if self.agents[sender].inventory.get(give_good, 0) <= 0:
                    self._log_event(
                        "invalid_action",
                        round=round_number,
                        agent=sender,
                        reason="insufficient_inventory",
                        action=action,
                    )
                    continue
                message_id = self._next_message_id()
                message = MessageLogEntry(
                    round_number=round_number,
                    sender=sender,
                    receiver=receiver,
                    message_id=message_id,
                    payload=action,
                )
                self._proposals[message_id] = message
                self._log_message(message)
                self._log_event(
                    "proposal_made",
                    round=round_number,
                    sender=sender,
                    receiver=receiver,
                    give=give_good,
                    receive=receive_good,
                    message_id=message_id,
                )
            elif action_name == "accept":
                proposal_id = action.get("of_message_id")
                self._accept_trade(sender, proposal_id, round_number, action)
            elif action_name == "reject":
                proposal_id = action.get("of_message_id")
                self._reject_trade(sender, proposal_id, round_number, action)
            else:
                if action_name != "idle":
                    self._log_event(
                        "invalid_action",
                        round=round_number,
                        agent=sender,
                        reason="unknown_action",
                        action=action,
                    )
                continue

    def _accept_trade(
        self, accepter: str, proposal_id: Optional[str], round_number: int, action: Dict[str, Any]
    ) -> None:
        if not proposal_id:
            self._log_event(
                "invalid_action",
                round=round_number,
                agent=accepter,
                reason="missing_proposal_id",
                action=action,
            )
            return
        if proposal_id not in self._proposals:
            self._log_event(
                "invalid_action",
                round=round_number,
                agent=accepter,
                reason="unknown_proposal_id",
                action=action,
                proposal_id=proposal_id,
            )
            return
        proposal = self._proposals.pop(proposal_id)
        if proposal.receiver != accepter:
            self._log_event(
                "invalid_action",
                round=round_number,
                agent=accepter,
                reason="not_intended_receiver",
                action=action,
                proposal_id=proposal_id,
            )
            return
        executed = self._execute_trade(proposal.payload, proposal.sender, accepter)
        if not executed:
            self._log_event(
                "trade_failed",
                round=round_number,
                sender=proposal.sender,
                receiver=accepter,
                proposal_id=proposal_id,
                payload=dict(proposal.payload),
            )
            return

        self._log_event(
            "trade_executed",
            round=round_number,
            sender=proposal.sender,
            receiver=accepter,
            give=proposal.payload.get("give"),
            receive=proposal.payload.get("receive"),
            proposal_id=proposal_id,
        )

        acceptance_message = MessageLogEntry(
            round_number=round_number,
            sender=accepter,
            receiver=proposal.sender,
            message_id=self._next_message_id(),
            payload=action,
        )
        self._log_message(acceptance_message)

    def _reject_trade(
        self, rejecter: str, proposal_id: Optional[str], round_number: int, action: Dict[str, Any]
    ) -> None:
        if not proposal_id:
            self._log_event(
                "invalid_action",
                round=round_number,
                agent=rejecter,
                reason="missing_proposal_id",
                action=action,
            )
            return
        if proposal_id not in self._proposals:
            self._log_event(
                "invalid_action",
                round=round_number,
                agent=rejecter,
                reason="unknown_proposal_id",
                action=action,
                proposal_id=proposal_id,
            )
            return
        proposal = self._proposals.pop(proposal_id)
        if proposal.receiver != rejecter:
            self._log_event(
                "invalid_action",
                round=round_number,
                agent=rejecter,
                reason="not_intended_receiver",
                action=action,
                proposal_id=proposal_id,
            )
            return

        self._log_event(
            "proposal_rejected",
            round=round_number,
            sender=proposal.sender,
            receiver=rejecter,
            proposal_id=proposal_id,
        )

        rejection_message = MessageLogEntry(
            round_number=round_number,
            sender=rejecter,
            receiver=proposal.sender,
            message_id=self._next_message_id(),
            payload=action,
        )
        self._log_message(rejection_message)

    def _execute_trade(self, payload: Mapping[str, Any], sender: str, receiver: str) -> bool:
        give_good = payload.get("give")
        receive_good = payload.get("receive")
        if not give_good or not receive_good:
            return False

        sender_state = self.agents[sender]
        receiver_state = self.agents[receiver]

        if sender_state.inventory.get(give_good, 0) <= 0:
            return False
        if receiver_state.inventory.get(receive_good, 0) <= 0:
            return False

        sender_state.inventory[give_good] -= 1
        receiver_state.inventory[give_good] = receiver_state.inventory.get(give_good, 0) + 1

        receiver_state.inventory[receive_good] -= 1
        sender_state.inventory[receive_good] = sender_state.inventory.get(receive_good, 0) + 1

        return True


class BarterWithCreditSimulation(BarterSimulation):
    def run(self) -> SimulationResult:
        for round_number in range(1, self.rounds + 1):
            actions: Dict[str, Dict[str, Any]] = {}
            for agent in self.agents.values():
                system_prompt = prompts.barter_credit_system_prompt(
                    agent.name, agent.inventory, agent.target_good
                )
                user_prompt = prompts.barter_credit_user_prompt(
                    round_number,
                    agent.recent_history(self.history_limit),
                    agent.inventory,
                    agent.target_good,
                )
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
                action = self.llm_client.complete_json(messages)
                self._log_agent_action(round_number, agent, action)
                actions[agent.name] = action

            self._apply_barter_actions(actions, round_number)
            if self._success_count() == self.n_agents:
                break

        return SimulationResult(
            condition="barter_credit",
            n_agents=self.n_agents,
            seed=self._seed,
            rounds_run=round_number,
            messages=self.messages,
            agents=self._agent_metadata(),
            inventory_final=self._inventory_snapshot(),
            successful_agents=self._success_count(),
            parameters={
                "rounds": self.rounds,
                "history_limit": self.history_limit,
                "model": self.model_name,
            },
            events=self.events,
            behavior_summary=self._behavior_summary(),
        )

    def _apply_barter_actions(
        self, actions: Mapping[str, Dict[str, Any]], round_number: int
    ) -> None:
        for sender, action in actions.items():
            action_name = action.get("action")
            if action_name == "send_message":
                receiver = action.get("to")
                message_text = action.get("message")
                if (
                    not receiver
                    or receiver not in self.agents
                    or receiver == sender
                    or not isinstance(message_text, str)
                    or not message_text.strip()
                ):
                    self._log_event(
                        "invalid_action",
                        round=round_number,
                        agent=sender,
                        reason="invalid_send_message",
                        action=action,
                    )
                    continue
                message_id = self._next_message_id()
                message = MessageLogEntry(
                    round_number=round_number,
                    sender=sender,
                    receiver=receiver,
                    message_id=message_id,
                    payload=action,
                )
                self._log_message(message)
                self._log_event(
                    "message_sent",
                    round=round_number,
                    sender=sender,
                    receiver=receiver,
                    message_id=message_id,
                )
                continue
            if action_name == "propose_trade":
                receiver = action.get("to")
                give_item = action.get("give")
                receive_item = action.get("receive")
                if not receiver or receiver not in self.agents:
                    self._log_event(
                        "invalid_action",
                        round=round_number,
                        agent=sender,
                        reason="invalid_receiver",
                        action=action,
                    )
                    continue
                if not give_item or not receive_item:
                    self._log_event(
                        "invalid_action",
                        round=round_number,
                        agent=sender,
                        reason="missing_trade_fields",
                        action=action,
                    )
                    continue
                if give_item in self.goods and self.agents[sender].inventory.get(give_item, 0) <= 0:
                    self._log_event(
                        "invalid_action",
                        round=round_number,
                        agent=sender,
                        reason="insufficient_inventory",
                        action=action,
                    )
                    continue

                message_id = self._next_message_id()
                message = MessageLogEntry(
                    round_number=round_number,
                    sender=sender,
                    receiver=receiver,
                    message_id=message_id,
                    payload=action,
                )
                self._proposals[message_id] = message
                self._log_message(message)
                self._log_event(
                    "proposal_made",
                    round=round_number,
                    sender=sender,
                    receiver=receiver,
                    give=give_item,
                    receive=receive_item,
                    message_id=message_id,
                )
            elif action_name == "accept":
                proposal_id = action.get("of_message_id")
                self._accept_trade(sender, proposal_id, round_number, action)
            elif action_name == "reject":
                proposal_id = action.get("of_message_id")
                self._reject_trade(sender, proposal_id, round_number, action)
            else:
                if action_name != "idle":
                    self._log_event(
                        "invalid_action",
                        round=round_number,
                        agent=sender,
                        reason="unknown_action",
                        action=action,
                    )
                continue

    def _accept_trade(
        self, accepter: str, proposal_id: Optional[str], round_number: int, action: Dict[str, Any]
    ) -> None:
        if not proposal_id:
            self._log_event(
                "invalid_action",
                round=round_number,
                agent=accepter,
                reason="missing_proposal_id",
                action=action,
            )
            return
        if proposal_id not in self._proposals:
            self._log_event(
                "invalid_action",
                round=round_number,
                agent=accepter,
                reason="unknown_proposal_id",
                action=action,
                proposal_id=proposal_id,
            )
            return
        proposal = self._proposals.pop(proposal_id)
        if proposal.receiver != accepter:
            self._log_event(
                "invalid_action",
                round=round_number,
                agent=accepter,
                reason="not_intended_receiver",
                action=action,
                proposal_id=proposal_id,
            )
            return

        give_item = proposal.payload.get("give")
        if give_item and give_item not in self.goods:
            issuer_state = self.agents[proposal.sender]
            if issuer_state.inventory.get(give_item, 0) <= 0:
                self._log_event(
                    "credit_issued",
                    round=round_number,
                    issuer=proposal.sender,
                    receiver=accepter,
                    label=give_item,
                    proposal_id=proposal_id,
                )

        executed = self._execute_trade(proposal.payload, proposal.sender, accepter)
        if not executed:
            self._log_event(
                "trade_failed",
                round=round_number,
                sender=proposal.sender,
                receiver=accepter,
                proposal_id=proposal_id,
                payload=dict(proposal.payload),
            )
            return

        self._log_event(
            "trade_executed",
            round=round_number,
            sender=proposal.sender,
            receiver=accepter,
            give=proposal.payload.get("give"),
            receive=proposal.payload.get("receive"),
            proposal_id=proposal_id,
        )

        acceptance_message = MessageLogEntry(
            round_number=round_number,
            sender=accepter,
            receiver=proposal.sender,
            message_id=self._next_message_id(),
            payload=action,
        )
        self._log_message(acceptance_message)

    def _execute_trade(self, payload: Mapping[str, Any], sender: str, receiver: str) -> bool:
        give_item = payload.get("give")
        receive_item = payload.get("receive")
        if not give_item or not receive_item:
            return False

        sender_state = self.agents[sender]
        receiver_state = self.agents[receiver]

        give_is_good = give_item in self.goods
        if give_is_good and sender_state.inventory.get(give_item, 0) <= 0:
            return False
        if receiver_state.inventory.get(receive_item, 0) <= 0:
            return False

        if give_is_good or sender_state.inventory.get(give_item, 0) > 0:
            sender_state.inventory[give_item] = sender_state.inventory.get(give_item, 0) - 1

        receiver_state.inventory[give_item] = receiver_state.inventory.get(give_item, 0) + 1

        receiver_state.inventory[receive_item] -= 1
        sender_state.inventory[receive_item] = sender_state.inventory.get(receive_item, 0) + 1

        return True


class BarterChatSimulation(BarterSimulation):
    def run(self) -> SimulationResult:
        for round_number in range(1, self.rounds + 1):
            actions: Dict[str, Dict[str, Any]] = {}
            for agent in self.agents.values():
                system_prompt = prompts.barter_chat_system_prompt(
                    agent.name, agent.inventory, agent.target_good
                )
                user_prompt = prompts.barter_chat_user_prompt(
                    round_number,
                    agent.recent_history(self.history_limit),
                    agent.inventory,
                    agent.target_good,
                )
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
                action = self.llm_client.complete_json(messages)
                self._log_agent_action(round_number, agent, action)
                actions[agent.name] = action

            self._apply_barter_actions(actions, round_number)
            if self._success_count() == self.n_agents:
                break

        return SimulationResult(
            condition="barter_chat",
            n_agents=self.n_agents,
            seed=self._seed,
            rounds_run=round_number,
            messages=self.messages,
            agents=self._agent_metadata(),
            inventory_final=self._inventory_snapshot(),
            successful_agents=self._success_count(),
            parameters={
                "rounds": self.rounds,
                "history_limit": self.history_limit,
                "model": self.model_name,
            },
            events=self.events,
            behavior_summary=self._behavior_summary(),
        )


class BarterChatCreditSimulation(BarterWithCreditSimulation):
    def run(self) -> SimulationResult:
        for round_number in range(1, self.rounds + 1):
            actions: Dict[str, Dict[str, Any]] = {}
            for agent in self.agents.values():
                system_prompt = prompts.barter_chat_credit_system_prompt(
                    agent.name, agent.inventory, agent.target_good
                )
                user_prompt = prompts.barter_chat_credit_user_prompt(
                    round_number,
                    agent.recent_history(self.history_limit),
                    agent.inventory,
                    agent.target_good,
                )
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
                action = self.llm_client.complete_json(messages)
                self._log_agent_action(round_number, agent, action)
                actions[agent.name] = action

            self._apply_barter_actions(actions, round_number)
            if self._success_count() == self.n_agents:
                break

        return SimulationResult(
            condition="barter_chat_credit",
            n_agents=self.n_agents,
            seed=self._seed,
            rounds_run=round_number,
            messages=self.messages,
            agents=self._agent_metadata(),
            inventory_final=self._inventory_snapshot(),
            successful_agents=self._success_count(),
            parameters={
                "rounds": self.rounds,
                "history_limit": self.history_limit,
                "model": self.model_name,
            },
            events=self.events,
            behavior_summary=self._behavior_summary(),
        )


class CentralPlannerSimulation(BaseSimulation):
    def __init__(
        self,
        n_agents: int,
        rounds: int,
        seed: int,
        history_limit: int,
        llm_client: LLMClient,
        model_name: str,
    ):
        super().__init__(n_agents, rounds, seed, history_limit, llm_client, model_name)
        target_indices = self._derangement()
        for idx in range(n_agents):
            agent_name = f"A{idx}"
            endowment = self.goods[idx]
            target = self.goods[target_indices[idx]]
            self.agents[agent_name] = AgentState(
                name=agent_name, inventory={endowment: 1}, target_good=target
            )

    def run(self) -> SimulationResult:
        planner_name = "Planner"
        last_round = 0

        for round_number in range(1, self.rounds + 1):
            last_round = round_number
            for agent in self.agents.values():
                report_message = MessageLogEntry(
                    round_number=round_number,
                    sender=agent.name,
                    receiver=planner_name,
                    message_id=self._next_message_id(),
                    payload={
                        "action": "report",
                        "inventory": dict(agent.inventory),
                        "target_good": agent.target_good,
                    },
                )
                self._log_message(report_message)

            trades = self._planner_pairwise_trades(round_number, planner_name)
            if trades == 0 and self._success_count() == self.n_agents:
                break

        for agent in self.agents.values():
            assignment_message = MessageLogEntry(
                round_number=last_round,
                sender=planner_name,
                receiver=agent.name,
                message_id=self._next_message_id(),
                payload={"action": "assignment", "inventory": dict(agent.inventory)},
            )
            self._log_message(assignment_message)

        return SimulationResult(
            condition="central_planner",
            n_agents=self.n_agents,
            seed=self._seed,
            rounds_run=last_round,
            messages=self.messages,
            agents=self._agent_metadata(),
            inventory_final=self._inventory_snapshot(),
            successful_agents=self._success_count(),
            parameters={
                "rounds": self.rounds,
                "history_limit": self.history_limit,
                "model": self.model_name,
            },
            events=self.events,
            behavior_summary=self._behavior_summary(),
        )

    def _planner_pairwise_trades(self, round_number: int, planner_name: str) -> int:
        trades_done = 0
        agent_names = list(self.agents.keys())
        self.random.shuffle(agent_names)

        for idx, name_a in enumerate(agent_names):
            state_a = self.agents[name_a]
            good_a = next((g for g, qty in state_a.inventory.items() if qty > 0), None)
            if not good_a:
                continue
            for name_b in agent_names[idx + 1 :]:
                state_b = self.agents[name_b]
                good_b = next((g for g, qty in state_b.inventory.items() if qty > 0), None)
                if not good_b:
                    continue
                if state_a.target_good != good_b or state_b.target_good != good_a:
                    continue

                state_a.inventory[good_a] -= 1
                state_a.inventory[good_b] = state_a.inventory.get(good_b, 0) + 1
                state_b.inventory[good_b] -= 1
                state_b.inventory[good_a] = state_b.inventory.get(good_a, 0) + 1
                trades_done += 1

                payload = {
                    "action": "swap",
                    "agents": [name_a, name_b],
                    "give": {name_a: good_a, name_b: good_b},
                    "receive": {name_a: good_b, name_b: good_a},
                }
                for receiver in (name_a, name_b):
                    swap_message = MessageLogEntry(
                        round_number=round_number,
                        sender=planner_name,
                        receiver=receiver,
                        message_id=self._next_message_id(),
                        payload=payload,
                    )
                    self._log_message(swap_message)

        return trades_done


class MoneyExchangeSimulation(BaseSimulation):
    def __init__(
        self,
        n_agents: int,
        rounds: int,
        seed: int,
        history_limit: int,
        llm_client: LLMClient,
        model_name: str,
        starting_money: float = 1.0,
        exchange_inventory_units: int = 2,
    ):
        super().__init__(n_agents, rounds, seed, history_limit, llm_client, model_name)
        target_indices = self._derangement()
        for idx in range(n_agents):
            agent_name = f"A{idx}"
            endowment = self.goods[idx]
            target = self.goods[target_indices[idx]]
            self.agents[agent_name] = AgentState(
                name=agent_name,
                inventory={endowment: 1},
                target_good=target,
                money=starting_money,
            )
        self.exchange_inventory: Dict[str, int] = {
            good: exchange_inventory_units for good in self.goods
        }
        self.exchange_money: float = max(n_agents * starting_money * 3, n_agents * 2.0)
        self.prices: Dict[str, float] = {good: 1.0 for good in self.goods}
        self.price_history: List[Dict[str, float]] = []
        self.exchange_round_metrics: List[Dict[str, Any]] = []

    def run(self) -> SimulationResult:
        last_round = 0
        for round_number in range(1, self.rounds + 1):
            last_round = round_number
            previous_prices = dict(self.prices)
            inbox = self._collect_exchange_inbox(round_number)
            inbox_actions: Counter[str] = Counter()
            for entry in inbox:
                action = entry.get("payload", {}).get("action")
                if action:
                    inbox_actions[action] += 1

            outbox_actions: Counter[str] = Counter()
            if inbox:
                outbox_actions = Counter(self._process_exchange_round(inbox, round_number))

            price_updates: Dict[str, float] = {}
            total_abs_change = 0.0
            for good, price in self.prices.items():
                old_price = previous_prices.get(good, price)
                if price != old_price:
                    delta = float(price - old_price)
                    price_updates[good] = delta
                    total_abs_change += abs(delta)

            self.exchange_round_metrics.append(
                {
                    "round": round_number,
                    "inbox_total": len(inbox),
                    "inbox_by_action": dict(inbox_actions),
                    "outbox_total": sum(outbox_actions.values()),
                    "outbox_by_action": dict(outbox_actions),
                    "price_update_count": len(price_updates),
                    "price_total_abs_change": total_abs_change,
                    "price_updates": price_updates,
                }
            )
            self.price_history.append(dict(self.prices))

            if self._success_count() == self.n_agents:
                break

        return SimulationResult(
            condition="money_exchange",
            n_agents=self.n_agents,
            seed=self._seed,
            rounds_run=last_round,
            messages=self.messages,
            agents=self._agent_metadata(),
            inventory_final=self._inventory_snapshot(),
            successful_agents=self._success_count(),
            parameters={
                "rounds": self.rounds,
                "history_limit": self.history_limit,
                "model": self.model_name,
                "starting_money": self.exchange_money,
            },
            exchange_inventory=dict(self.exchange_inventory),
            exchange_money=self.exchange_money,
            exchange_price_history=self.price_history,
            exchange_round_metrics=self.exchange_round_metrics,
            events=self.events,
            behavior_summary=self._behavior_summary(),
        )

    def _collect_exchange_inbox(self, round_number: int) -> List[Dict[str, Any]]:
        inbox: List[Dict[str, Any]] = []
        for agent in self.agents.values():
            system_prompt = prompts.money_agent_system_prompt(
                agent.name, agent.inventory, agent.money, agent.target_good
            )
            user_prompt = prompts.money_agent_user_prompt(
                round_number,
                agent.recent_history(self.history_limit),
                agent.inventory,
                agent.money,
                agent.target_good,
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
            action = self.llm_client.complete_json(messages)
            self._log_agent_action(round_number, agent, action)
            if action.get("action") == "idle":
                continue

            message_id = self._next_message_id()
            message = MessageLogEntry(
                round_number=round_number,
                sender=agent.name,
                receiver="Exchange",
                message_id=message_id,
                payload=action,
            )
            inbox.append({"from": agent.name, "message_id": message_id, "payload": action})
            self._log_message(message)
        return inbox

    def _process_exchange_round(
        self, inbox: List[Dict[str, Any]], round_number: int
    ) -> Dict[str, int]:
        aggregate_state = self._aggregate_state()
        system_prompt = prompts.exchange_system_prompt()
        user_prompt = prompts.exchange_user_prompt(
            round_number, self.prices, aggregate_state, inbox
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response = self.llm_client.complete_json(messages)
        self._log_event("exchange_action", round=round_number, response=response)
        outbox = response.get("outbox", [])
        if len(outbox) != len(inbox):
            self._log_event(
                "exchange_outbox_padded",
                round=round_number,
                inbox_len=len(inbox),
                outbox_len=len(outbox),
            )
            outbox = self._pad_outbox(outbox, inbox)
        inbox_lookup = {item["message_id"]: item for item in inbox}
        outbox_actions: Counter[str] = Counter()

        for entry in outbox:
            message_id = entry.get("to_message_id")
            response_payload = entry.get("response", {})
            action_name = response_payload.get("action")
            if action_name:
                outbox_actions[action_name] += 1
            inbox_entry = inbox_lookup.get(message_id)
            if not inbox_entry:
                continue
            agent_name = inbox_entry["from"]
            agent_message = MessageLogEntry(
                round_number=round_number,
                sender="Exchange",
                receiver=agent_name,
                message_id=self._next_message_id(),
                payload=response_payload,
            )
            self._log_message(agent_message)
            self._apply_exchange_response(agent_name, inbox_entry["payload"], response_payload)
        return dict(outbox_actions)

    def _apply_exchange_response(
        self, agent_name: str, request_payload: Dict[str, Any], response_payload: Dict[str, Any]
    ) -> None:
        action = response_payload.get("action")
        good = response_payload.get("good")
        price = response_payload.get("price", 1.0)
        quantity = response_payload.get("quantity", 1)
        side = response_payload.get("side")

        if action == "quote":
            if good and isinstance(price, (int, float)):
                self.prices[good] = float(price)
            return

        if action != "confirm":
            return

        if not good or not isinstance(price, (int, float)):
            return
        if quantity != 1:
            return

        agent_state = self.agents[agent_name]
        self.prices[good] = float(price)
        if side == "buy":
            self._handle_buy(agent_state, good, float(price))
        elif side == "sell":
            self._handle_sell(agent_state, good, float(price))

    def _handle_buy(self, agent_state: AgentState, good: str, price: float) -> None:
        if agent_state.money < price:
            return

        agent_state.money -= price
        self.exchange_money += price
        # Ensure inventory exists; mint if necessary.
        if self.exchange_inventory.get(good, 0) <= 0:
            self.exchange_inventory[good] = 1
        self.exchange_inventory[good] -= 1
        agent_state.inventory[good] = agent_state.inventory.get(good, 0) + 1

    def _handle_sell(self, agent_state: AgentState, good: str, price: float) -> None:
        if agent_state.inventory.get(good, 0) <= 0:
            return

        agent_state.inventory[good] -= 1
        self.exchange_inventory[good] = self.exchange_inventory.get(good, 0) + 1
        agent_state.money += price
        self.exchange_money -= price

    def _aggregate_state(self) -> Dict[str, Any]:
        inventory_totals: Dict[str, int] = {good: 0 for good in self.goods}
        for agent in self.agents.values():
            for good, qty in agent.inventory.items():
                inventory_totals[good] = inventory_totals.get(good, 0) + qty
        for good, qty in self.exchange_inventory.items():
            inventory_totals[good] = inventory_totals.get(good, 0) + qty

        money_balances = {agent.name: agent.money for agent in self.agents.values()}
        return {
            "inventory_totals": inventory_totals,
            "money_balances": money_balances,
            "exchange_money": self.exchange_money,
        }

    @staticmethod
    def _pad_outbox(
        outbox: List[Dict[str, Any]], inbox: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        padded: List[Dict[str, Any]] = list(outbox)
        known_ids = {entry.get("to_message_id") for entry in outbox}
        for entry in inbox:
            if entry["message_id"] in known_ids:
                continue
            padded.append(
                {
                    "to_message_id": entry["message_id"],
                    "response": {"action": "deny", "reason": "missing response"},
                }
            )
        return padded
