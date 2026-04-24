#!/usr/bin/env python3
# week4: Multi-tool agent demonstrating tool chaining
# Scenario: User asks for stock price, then asks to calculate percentage change.
# Tools: StockPrice (fake), Calculator, Search (for company name fallback)
# Demonstrates: Tool selection, chaining, and handling multi-step reasoning.

import os
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain.tools import Tool

def get_llm():
    try:
        return OpenAI(temperature=0)
    except Exception:
        from langchain.llms.fake import FakeListLLM
        # Provide a sequence that simulates ReAct for a two-step question
        return FakeListLLM(responses=[
            # First question: "What is the current price of Apple stock?"
            "Thought: I need to get the current stock price for Apple.\nAction: StockPrice\nAction Input: AAPL",
            # Observation: (we simulate observation in the tool)
            "Thought: Now I have the price. The user also asked for percentage change from last week's price of $150.\nAction: Calculator\nAction Input: (170-150)/150*100",
            # Second question in same run? Actually we'll handle separate invocations.
        ])

# Mock stock price tool (replace with real API like yfinance or Alpha Vantage)
def stock_price_tool(symbol: str) -> str:
    """Return a fake current price for demo. In real use, call a financial API."""
    # Simulate known prices
    prices = {"AAPL": "170.00", "GOOGL": "130.00", "MSFT": "320.00"}
    price = prices.get(symbol.upper())
    if price is None:
        return f"Sorry, I don't have data for {symbol}."
    return f"The current price of {symbol.upper()} is ${price}."

def calculator_tool(expression: str) -> str:
    """Safe calculator for basic arithmetic."""
    try:
        allowed = set('0123456789+-*/().% ')
        if not all(c in allowed for c in expression):
            return "Error: Invalid characters in expression."
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"

def search_tool(query: str) -> str:
    """Fallback to get company symbol from name."""
    # Very naive mapping for demo
    name_to_symbol = {
        "apple": "AAPL",
        "google": "GOOGL",
        "microsoft": "MSFT",
        "tesla": "TSLA"
    }
    query_lower = query.lower()
    for name, sym in name_to_symbol.items():
        if name in query_lower:
            return f"The stock symbol for {name} is {sym}."
    return f"Could not determine symbol for '{query}'. Try providing the ticker symbol."

def main():
    llm = get_llm()
    tools = [
        Tool(
            name="StockPrice",
            func=stock_price_tool,
            description="Get current stock price for a given ticker symbol. Input: stock ticker (e.g., AAPL)."
        ),
        Tool(
            name="Calculator",
            func=calculator_tool,
            description="Perform mathematical calculations. Input: a valid arithmetic expression."
        ),
        Tool(
            name="SearchSymbol",
            func=search_tool,
            description="Find stock ticker symbol from company name. Input: company name or partial name."
        )
    ]

    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    print("\n=== Multi-tool Agent Demo ===")
    print("Example 1: Get stock price")
    print("Q: What is the current price of Apple stock?")
    resp1 = agent.run("What is the current price of Apple stock?")
    print(f"A: {resp1}")

    print("\nExample 2: Calculate percentage change")
    print('Q: If Apple stock was $150 last week, what is the percentage change to current price?')
    # We need to provide the current price; agent could fetch it then compute.
    resp2 = agent.run("If Apple stock was $150 last week, what is the percentage change to current price?")
    print(f"A: {resp2}")

    print("\nExample 3: Using search to get symbol then price")
    print('Q: What is the current price of Google?')
    resp3 = agent.run("What is the current price of Google?")
    print(f"A: {resp3}")

if __name__ == "__main__":
    main()