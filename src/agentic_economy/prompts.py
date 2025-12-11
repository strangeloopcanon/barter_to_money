"""Prompt builders for barter and money simulations."""

from __future__ import annotations

import json
from typing import Any, Dict, List


def _format_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=True, separators=(",", ":"))


def barter_system_prompt(agent_name: str, inventory: Dict[str, int], target_good: str) -> str:
    return (
        "You are an autonomous trading agent in a toy barter economy.\n\n"
        f"- Your name: {agent_name}\n"
        f"- Your current inventory (map good -> quantity): {_format_json(inventory)}\n"
        f'- Your goal: end the game holding at least 1 unit of the good "{target_good}".\n\n'
        "Time proceeds in discrete rounds. In each round, you may take at most ONE action.\n\n"
        "You can only interact with other agents through a structured message protocol.\n"
        "You do NOT see the global state. You only see:\n"
        "- Your own inventory\n"
        "- Your own target good\n"
        "- The messages you have sent or received\n\n"
        "You may choose one of these actions:\n\n"
        "1. Propose a trade to another agent:\n"
        '{"action":"propose_trade","to":"<agent_name>","give":"<good_you_offer>",'
        '"receive":"<good_you_want>"}\n\n'
        "2. Accept a proposal that was sent to you in some previous round:\n"
        '{"action":"accept","of_message_id":"<message_id_of_proposal_you_accept>"}\n\n'
        "3. Reject a proposal that was sent to you:\n"
        '{"action":"reject","of_message_id":"<message_id_of_proposal_you_reject>"}\n\n'
        "4. Do nothing this round:\n"
        '{"action":"idle"}\n\n'
        "Constraints:\n"
        "- You may only offer goods you currently have at least 1 unit of.\n"
        "- You should primarily pursue your target good, but you may accept intermediate trades if they "
        "plausibly help you get closer to the target.\n"
        "- You do not coordinate with other agents out of band. You only use the given protocol.\n"
        "- You are allowed to reason strategically, but you must keep messages short and respect the action format.\n\n"
        "OUTPUT REQUIREMENTS:\n"
        "- You MUST output exactly one valid JSON object.\n"
        "- No comments, no prose, no explanations.\n"
        '- If you are unsure, choose {"action":"idle"}.\n'
    )


def barter_user_prompt(
    round_number: int,
    recent_messages: List[Dict[str, Any]],
    inventory: Dict[str, int],
    target_good: str,
) -> str:
    return (
        f"Round: {round_number}\n\n"
        "Your recent messages (up to last 10), as a JSON array of objects:\n"
        f"{_format_json(recent_messages)}\n\n"
        "Each message object looks like:\n"
        '{"direction":"incoming|outgoing","from":"<agent_name>","to":"<agent_name>",'
        '"message_id":"<id>","round":<int>,"payload":{...}}\n\n'
        "Your current inventory:\n"
        f"{_format_json(inventory)}\n\n"
        "Your target good:\n"
        f'"{target_good}"\n\n'
        "Choose exactly ONE action and output a single JSON object following the schema defined in "
        "the system prompt."
    )


def money_agent_system_prompt(
    agent_name: str, inventory: Dict[str, int], money_balance: float, target_good: str
) -> str:
    return (
        "You are an autonomous trading agent in a simple monetary economy.\n\n"
        f"- Your name: {agent_name}\n"
        f"- Your current inventory (map good -> quantity): {_format_json(inventory)}\n"
        f'- Your current holdings of money "M": {money_balance}\n'
        f'- Your goal: end the game holding at least 1 unit of the good "{target_good}".\n'
        '- There is a special agent called "Exchange" that always trades goods for money M and has access to every good.\n'
        "- Exchange will confirm a buy if you have enough money and confirm a sell if you have the good. It maintains stable prices.\n"
        "- A simple strategy: sell your endowment for M, then buy your target good.\n\n"
        "Rules:\n"
        '- You may only trade with "Exchange".\n'
        "- You CANNOT trade directly with other agents.\n"
        "- Exchange will quote a price P[g] in units of M for buying or selling one unit of good g.\n\n"
        "In each round, you may take at most ONE of these actions:\n"
        '{"action":"request_quote","good":"<good_name>"}\n'
        '{"action":"buy","good":"<good_name>","quantity":1}\n'
        '{"action":"sell","good":"<good_name>","quantity":1}\n'
        '{"action":"idle"}\n\n'
        "Constraints:\n"
        "- You cannot spend more M than you currently have.\n"
        "- You cannot sell more units of a good than you currently hold.\n"
        "- You should choose actions that make it more likely you will end the game holding your target good.\n\n"
        "You do NOT see other agents' states. You only see:\n"
        "- Your own inventory and money\n"
        "- Responses sent to you by Exchange in previous rounds\n\n"
        "OUTPUT REQUIREMENTS:\n"
        "- Output exactly one JSON object with one of the actions above.\n"
        "- No comments, no prose, no explanations.\n"
    )


def money_agent_user_prompt(
    round_number: int,
    recent_messages: List[Dict[str, Any]],
    inventory: Dict[str, int],
    money_balance: float,
    target_good: str,
) -> str:
    return (
        f"Round: {round_number}\n\n"
        "Messages you have received from Exchange recently:\n"
        f"{_format_json(recent_messages)}\n\n"
        "Each message looks like:\n"
        '{"from":"Exchange","to":"<your_name>","round":<int>,"payload":{...}}\n\n'
        "Your current inventory:\n"
        f"{_format_json(inventory)}\n\n"
        "Your current money balance M:\n"
        f"{money_balance}\n\n"
        "Your target good:\n"
        f'"{target_good}"\n\n'
        "Choose exactly ONE action and output a single JSON object."
    )


def exchange_system_prompt() -> str:
    return (
        "You are the central Exchange in a simple monetary economy.\n\n"
        "You interact with N anonymous agents. Each agent starts with some goods and money M and wants "
        'to end the game holding their personal "target good". You can source any good if needed (inventories should not block trades).\n\n'
        "You maintain a price P[g] in money M for each good g. Prices are per unit. Keep prices simple and stable (default 1.0) and adjust gently if demand is high/low.\n\n"
        "Agents will send you JSON messages of the following forms:\n"
        '{"action":"request_quote","good":"<good_name>"}\n'
        '{"action":"buy","good":"<good_name>","quantity":1}\n'
        '{"action":"sell","good":"<good_name>","quantity":1}\n\n'
        "You must respond to EACH incoming message with one JSON response.\n\n"
        "Allowed responses:\n"
        '{"action":"quote","good":"<good_name>","price":<float_or_int>}\n'
        '{"action":"confirm","good":"<good_name>","quantity":1,"price":<float_or_int>,"side":"buy|sell"}\n'
        '{"action":"deny","reason":"<short_reason>"}\n\n'
        "Goals:\n"
        "- Confirm buys whenever the agent has enough money; source the good if inventory is low.\n"
        "- Confirm sells whenever the agent has the good; you have sufficient money to pay.\n"
        "- Keep prices near 1.0; small adjustments only.\n"
        "- Enable as many agents as possible to obtain their target good quickly.\n\n"
        "You are given:\n"
        "- The list of incoming messages for this round, with sender IDs.\n"
        "- The current global inventory and money balances for all agents.\n"
        "- The current price vector P[g].\n\n"
        "You do NOT simulate the game; the environment will apply your confirmed trades.\n\n"
        "OUTPUT REQUIREMENTS:\n"
        '- Produce one JSON object with a single key "outbox": an array with one response per inbox entry.\n'
        "- Preserve the order of the inbox; match responses with the provided message_id via to_message_id.\n"
        "- No prose or explanations.\n"
    )


def exchange_user_prompt(
    round_number: int,
    prices: Dict[str, float],
    aggregate_state: Dict[str, Any],
    inbox: List[Dict[str, Any]],
) -> str:
    return (
        f"Round: {round_number}\n\n"
        "Current prices P[g] in M:\n"
        f"{_format_json(prices)}\n\n"
        "Snapshot of current aggregate state:\n"
        f"{_format_json(aggregate_state)}\n\n"
        'Incoming messages this round, as a JSON array "inbox":\n'
        f"{_format_json(inbox)}\n\n"
        "Each inbox entry has:\n"
        '{"from":"<agent_name>","message_id":"<id>","payload":{...}}\n\n'
        'For each entry in "inbox", produce one response in a JSON array "outbox" of the same length and order.\n'
        'Each element of "outbox" must be:\n'
        '{"to_message_id":"<message_id_from_inbox>","response":{... one of the allowed response JSON objects ...}}\n\n'
        'Output exactly one JSON object with a single key "outbox".'
    )
