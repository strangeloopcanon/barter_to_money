from __future__ import annotations

import json
from typing import Any, Dict

from agentic_economy.llm_client import LLMClient
from agentic_economy.simulation import BarterSimulation, MoneyExchangeSimulation


class DummyLLM:
    def complete_json(self, messages: Any) -> Dict[str, Any]:
        return {"action": "idle"}


def _extract_agent_name(messages: Any) -> str:
    for message in messages:
        if message.get("role") == "system":
            content: str = message.get("content", "")
            if "Your name:" in content:
                return content.split("Your name:")[1].split("\n")[0].strip()
    return "unknown"


class ScriptedBarterLLM:
    def __init__(self, script: Dict[str, list[Dict[str, Any]]]):
        self.script = script

    def complete_json(self, messages: Any) -> Dict[str, Any]:
        agent = _extract_agent_name(messages)
        actions = self.script.get(agent, [])
        if not actions:
            return {"action": "idle"}
        return actions.pop(0)


class ScriptedMoneyLLM:
    def __init__(self):
        self.agent_calls: Dict[str, int] = {}

    def complete_json(self, messages: Any) -> Dict[str, Any]:
        system_content = messages[0].get("content", "")
        if "central Exchange" in system_content:
            user_content = messages[1].get("content", "")
            inbox_raw = user_content.split('inbox":\n', 1)[1].split("\n\nEach inbox entry", 1)[0]
            inbox = json.loads(inbox_raw)
            outbox = []
            for item in inbox:
                payload = item["payload"]
                action = payload.get("action")
                good = payload.get("good")
                side = "sell" if action == "sell" else "buy"
                outbox.append(
                    {
                        "to_message_id": item["message_id"],
                        "response": {
                            "action": "confirm",
                            "good": good,
                            "quantity": 1,
                            "price": 1.0,
                            "side": side,
                        },
                    }
                )
            return {"outbox": outbox}

        agent = _extract_agent_name(messages)
        count = self.agent_calls.get(agent, 0)
        self.agent_calls[agent] = count + 1
        if agent == "A0":
            return (
                {"action": "sell", "good": "g0", "quantity": 1}
                if count == 0
                else {"action": "buy", "good": "g1", "quantity": 1}
            )
        if agent == "A1":
            return (
                {"action": "sell", "good": "g1", "quantity": 1}
                if count == 0
                else {"action": "buy", "good": "g0", "quantity": 1}
            )
        return {"action": "idle"}


def test_barter_targets_are_deranged() -> None:
    sim = BarterSimulation(
        n_agents=5,
        rounds=1,
        seed=42,
        history_limit=2,
        llm_client=DummyLLM(),  # type: ignore[arg-type]
        model_name="dummy",
    )
    for state in sim.agents.values():
        endowment = next(iter(state.inventory.keys()))
        assert endowment != state.target_good


def test_money_exchange_initial_state() -> None:
    sim = MoneyExchangeSimulation(
        n_agents=4,
        rounds=1,
        seed=1,
        history_limit=2,
        llm_client=DummyLLM(),  # type: ignore[arg-type]
        model_name="dummy",
        starting_money=1.0,
    )
    assert sim.exchange_money >= 4.0
    assert all(amount >= 1 for amount in sim.exchange_inventory.values())
    assert all(agent.money == 1.0 for agent in sim.agents.values())


def test_barter_run_completes_trade() -> None:
    script = {
        "A0": [
            {"action": "propose_trade", "to": "A1", "give": "g0", "receive": "g1"},
            {"action": "idle"},
        ],
        "A1": [
            {"action": "idle"},
            {"action": "accept", "of_message_id": "m0"},
        ],
    }
    sim = BarterSimulation(
        n_agents=2,
        rounds=2,
        seed=0,
        history_limit=5,
        llm_client=ScriptedBarterLLM(script),  # type: ignore[arg-type]
        model_name="dummy",
    )
    result = sim.run()
    assert result.successful_agents == 2
    assert result.inventory_final["A0"].get("g1", 0) == 1
    assert result.inventory_final["A1"].get("g0", 0) == 1


def test_money_exchange_round_trip() -> None:
    llm = ScriptedMoneyLLM()
    sim = MoneyExchangeSimulation(
        n_agents=2,
        rounds=2,
        seed=0,
        history_limit=4,
        llm_client=llm,  # type: ignore[arg-type]
        model_name="dummy",
        starting_money=1.0,
    )
    result = sim.run()
    assert result.successful_agents == 2
    assert result.exchange_inventory is not None
    assert result.exchange_inventory["g0"] >= 0
    assert result.exchange_inventory["g1"] >= 0


def test_extract_json_from_output_text() -> None:
    class FakeResponse:
        def __init__(self, content: str):
            self.output_text = content

    response = FakeResponse('{"action":"idle"}')
    data = LLMClient._extract_json(response)
    assert data["action"] == "idle"


def test_extract_json_from_nested_output() -> None:
    class ContentPart:
        def __init__(self, text: str):
            self.text = text

    class OutputEntry:
        def __init__(self, content: Any):
            self.content = content

    class FakeResponse:
        def __init__(self, output: Any):
            self.output = output

    response = FakeResponse([OutputEntry([ContentPart('{"action":"idle"}')])])
    data = LLMClient._extract_json(response)
    assert data["action"] == "idle"


def test_llm_client_complete_json_with_mock_client() -> None:
    class FakeResponses:
        def __init__(self, payload: Any):
            self.payload = payload

        def create(self, **_: Any) -> Any:
            return self.payload

    fake_response = type("Resp", (), {"output_text": '{"action":"idle"}'})()
    fake_client = type("FakeClient", (), {"responses": FakeResponses(fake_response)})()
    client = LLMClient(model="dummy", client=fake_client)
    action = client.complete_json([{"role": "user", "content": "hi"}])
    assert action["action"] == "idle"


class SparseExchangeLLM:
    def complete_json(self, messages: Any) -> Dict[str, Any]:
        system_content = messages[0].get("content", "")
        if "central Exchange" in system_content:
            return {"outbox": []}
        return {"action": "buy", "good": "g0", "quantity": 1}


def test_money_exchange_pads_outbox() -> None:
    sim = MoneyExchangeSimulation(
        n_agents=1,
        rounds=1,
        seed=0,
        history_limit=2,
        llm_client=SparseExchangeLLM(),  # type: ignore[arg-type]
        model_name="dummy",
        starting_money=1.0,
    )
    result = sim.run()
    assert result.messages
