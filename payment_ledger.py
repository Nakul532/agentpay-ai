"""
AgentPay AI - Mock USDC payment ledger.
Simulates on-chain settlement for agent-to-API payments.
"""
from datetime import datetime
import random
import string


def generate_txn_hash():
    """Generate a mock blockchain transaction hash."""
    return "0x" + "".join(random.choices(string.hexdigits.lower(), k=16)) + "..."


def execute_payment(agent, api, reasoning, response):
    """Execute a mock USDC payment from agent to API provider."""
    # Check balance
    if agent['current_balance'] < api['price']:
        return {
            "status": "failed",
            "reason": f"Insufficient balance: ${agent['current_balance']:.4f} < ${api['price']:.4f}",
        }

    # Check spending limit
    if api['price'] > agent['spending_limit_per_txn']:
        return {
            "status": "failed",
            "reason": f"Exceeds per-txn limit (${agent['spending_limit_per_txn']:.2f})",
        }

    # Settle payment
    agent['current_balance'] -= api['price']

    return {
        "status": "settled",
        "txn_hash": generate_txn_hash(),
        "block_number": random.randint(18_000_000, 19_000_000),
        "gas_used_usdc": 0.00012,
        "settlement_time_ms": random.randint(120, 380),
        "timestamp": datetime.utcnow().isoformat(),
        "from": agent['wallet_address'],
        "to": f"0x{api['provider'][:6].lower()}...api",
        "amount_usdc": api['price'],
        "agent_name": agent['name'],
        "agent_id": agent['id'],
        "api_name": api['name'],
        "api_provider": api['provider'],
        "api_category": api['category'],
        "reasoning": reasoning,
        "api_response": response,
    }
