#!/usr/bin/env python3
# week2: ReAct agent with tool usage (search + calculator)
# Demonstrates: AgentExecutor, Tools, ReAct pattern
# Requires: langchain, openai, duckduckgo-search, python-dotenv

import os
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain.tools import Tool
from duckduckgo_search import DDGS

# Optional: fake LLM for demo if no API key
def get_llm():
    try:
        return OpenAI(temperature=0)
    except Exception:
        from langchain.llms.fake import FakeListLLM
        # Provide some canned responses for demonstration
        return FakeListLLM(responses=[
            "Thought: I need to search for the capital of France.\nAction: Search\nAction Input: capital of France",
            "Observation: The capital of France is Paris.\nThought: Now I know the answer.\nAction: Finish\nAction Input: Paris"
        ])

def search_tool(query: str) -> str:
    """Simple wrapper around duckduckgo-search."""
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=3)
        if not results:
            return "No results found."
        # Return snippet of first result
        return results[0].get('body', 'No snippet')
    except Exception as e:
        return f"Search error: {e}"

def calculator_tool(expression: str) -> str:
    """Very basic calculator - for demo only, not safe for production."""
    try:
        # Only allow simple arithmetic for safety
        allowed = set('0123456789+-*/(). ')
        if not all(c in allowed for c in expression):
            return "Error: Invalid expression."
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"

def main():
    llm = get_llm()
    tools = [
        Tool(
            name="Search",
            func=search_tool,
            description="Useful for answering questions about current events or general knowledge. Input should be a search query."
        ),
        Tool(
            name="Calculator",
            func=calculator_tool,
            description="Useful for answering math questions. Input should be a mathematical expression."
        )
    ]

    # Initialize agent with ReAct style (zero-shot-react-description)
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    # Example questions
    questions = [
        "What is the capital of France?",
        "What is 25 * 4 + 10?"
    ]

    for q in questions:
        print(f"\nQuestion: {q}")
        try:
            response = agent.run(q)
            print(f"Answer: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()