# blockchainiq-x402-langchain

A minimal [LangChain](https://python.langchain.com/) tool that calls [Blockchain IQ](https://www.blockchainiq.co)'s pay-per-call crypto data API over the [x402](https://www.x402.org) payment standard (USDC on Base).

No account and no API key: the first request returns HTTP 402 with a price, the x402 client signs a USDC payment authorization (EIP-3009), retries, and gets JSON back.

## Resources used

| Resource | Path | Price |
| --- | --- | --- |
| brief | `GET /api/x402/v1/brief` | $0.01 |
| event-risk | `GET /api/x402/v1/event-risk` | $0.05 |

`brief` returns prices and recent moves for Bitcoin, Ethereum, Solana and XRP, scheduled events in the next 48 hours, and short risk flags. `event-risk` returns US data releases, central bank decisions, Treasury auctions and dated crypto/regulatory milestones, seven days ahead by default.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in a payer private key (Base, small USDC balance)
```

The payer key needs only a few cents of USDC on Base; the x402 facilitator submits the on-chain transaction, so no ETH for gas is required. Never commit a real key: `.env` is gitignored.

## Run

```bash
python main.py
```

This calls `brief` once ($0.01), prints the JSON, and prints the settlement transaction hash of the payment.

## Files

- `blockchainiq_tool.py` - the LangChain `@tool` definitions (`blockchainiq_brief`, `blockchainiq_event_risk`)
- `main.py` - a minimal demo that invokes the brief tool directly
- `.env.example` - the one environment variable you need

Made for the Blockchain IQ x402 integration bounty: https://www.blockchainiq.co/blog/x402-build-bounties
