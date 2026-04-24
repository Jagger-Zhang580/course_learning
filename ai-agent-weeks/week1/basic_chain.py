#!/usr/bin/env python3
# week1: basic LLM chain using LangChain
# Demonstrates: PromptTemplate + LLM + SimpleChain
# Requires: langchain, openai, python-dotenv
# Set OPENAI_API_KEY in .env or export

import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

load_dotenv()  # loads .env file

def build_chain():
    template = """You are a helpful assistant. Answer the question concisely.

Question: {question}
Answer:"""
    prompt = PromptTemplate(
        input_variables=["question"],
        template=template,
    )
    # Use OpenAI LLM; if no key, will raise error - we catch and use a fake LLM for demo
    try:
        llm = OpenAI(temperature=0)
    except Exception as e:
        print("Warning: OpenAI API key not found or invalid. Using dummy LLM.")
        from langchain.llms.fake import FakeListLLM
        llm = FakeListLLM(responses=["This is a dummy response. Set OPENAI_API_KEY to use real LLM."])
    return prompt | llm  # RunnableSequence

if __name__ == "__main__":
    chain = build_chain()
    question = "What is the capital of France?"
    print(f"Q: {question}")
    ans = chain.invoke({"question": question})
    print(f"A: {ans}")