"""Minimal demo: call Blockchain IQ's $0.01 brief resource through the LangChain tool."""

import json

from blockchainiq_tool import blockchainiq_brief

if __name__ == "__main__":
    result = blockchainiq_brief.invoke({})
    print(json.dumps(result, indent=2))
