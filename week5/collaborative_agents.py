#!/usr/bin/env python3
# week5: Two-agent collaboration (Researcher + Writer)
# Demonstrates: Sequential task decomposition, Agent communication via shared memory
# Requires: langchain, openai, python-dotenv

import os
from dotenv import load_dotenv
load_dotenv()

from langchain.llms import OpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def get_llm():
    try:
        return OpenAI(temperature=0)
    except Exception:
        from langchain.llms.fake import FakeListLLM
        # Provide canned responses for the two-agent flow
        return FakeListLLM(responses=[
            # Researcher: thinks about what to search
            "Thought: I need to gather info about renewable energy trends 2024.\nAction: Search\nAction Input: renewable energy trends 2024",
            # Observation (we will fake in tool)
            "Thought: I have found some info. Now I will summarize for the writer.\nAction: Finish\nAction Input: In 2024, renewable energy adoption grew rapidly, with solar and wind leading. Investment reached $1.7 trillion globally.",
            # Writer: receives the summary and writes a short report
            "Thought: I need to write a brief report based on the researcher's findings.\nAction: Finish\nAction Input: Renewable Energy Report 2024\nSummary: Renewable energy adoption accelerated in 2024, driven by solar and wind power. Global investment hit $1.7 trillion, marking a 20% increase from the previous year."
        ])

# Simple search tool (duckduckgo) for researcher
def search_tool(query: str) -> str:
    try:
        from duckduckgo_search import DDGS
        ddgs = DDGS()
        results = ddgs.text(query, max_results=3)
        if not results:
            return "No results found."
        return results[0].get('body', 'No snippet')
    except Exception as e:
        return f"Search error: {e}"

def main():
    llm = get_llm()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Tools for researcher
    tools = [
        Tool(
            name="Search",
            func=search_tool,
            description="Useful for answering questions about current events or general knowledge. Input should be a search query."
        )
    ]
    
    researcher = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory, verbose=True
    )
    
    # Writer uses a simple LLMChain with a prompt that expects a summary
    writer_prompt = PromptTemplate(
        input_variables=["research_summary"],
        template="You are a skilled writer. Based on the following research summary, write a concise report (2-3 paragraphs) suitable for a business audience.\n\nResearch Summary:\n{research_summary}\n\nReport:"
    )
    writer_llm = LLMChain(llm=llm, prompt=writer_prompt)
    
    print("=== Collaborative Agents Demo (Researcher + Writer) ===")
    task = "Renewable energy trends in 2024"
    print(f"\nTask: {task}")
    
    # Step 1: Researcher gathers info
    print("\n--- Researcher working ---")
    research_result = researcher.run(task)
    print(f"Researcher output: {research_result}")
    
    # Step 2: Writer produces report
    print("\n--- Writer working ---")
    report = writer_llm.run(research_summary=research_result)
    print(f"Writer output:\n{report}")
    
if __name__ == "__main__":
    main()