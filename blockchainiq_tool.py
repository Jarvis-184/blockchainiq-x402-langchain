"""LangChain tools for Blockchain IQ's x402 paid API (USDC on Base)."""

import os

from dotenv import load_dotenv
from eth_account import Account
from langchain_core.tools import tool
from x402.clients.httpx import x402HttpxClient

load_dotenv()

BASE_URL = "https://www.blockchainiq.co"
BRIEF_PATH = "/api/x402/v1/brief"
EVENT_RISK_PATH = "/api/x402/v1/event-risk"


def _make_client() -> x402HttpxClient:
    """Build an x402 httpx client from the payer key in the environment.

    The key signs EIP-3009 USDC payment authorizations on Base; the x402
    facilitator submits the on-chain transaction, so the wallet needs only a
    small USDC balance and no ETH for gas.
    """
    key = os.environ.get("BLOCKCHAINIQ_PAYER_KEY")
    if not key:
        raise RuntimeError("Set BLOCKCHAINIQ_PAYER_KEY in the environment (see .env.example).")
    return x402HttpxClient(account=Account.from_key(key))


def _paid_get(path: str) -> dict:
    with _make_client() as client:
        resp = client.get(BASE_URL + path)
        resp.raise_for_status()
        return resp.json()


@tool
def blockchainiq_brief() -> dict:
    """Prices and recent moves for BTC, ETH, SOL and XRP, scheduled events in
    the next 48 hours, and short risk flags. Costs $0.01 USDC on Base via x402."""
    return _paid_get(BRIEF_PATH)


@tool
def blockchainiq_event_risk() -> dict:
    """US data releases, central bank decisions, Treasury auctions and dated
    crypto/regulatory milestones, seven days ahead. Costs $0.05 USDC on Base via x402."""
    return _paid_get(EVENT_RISK_PATH)
