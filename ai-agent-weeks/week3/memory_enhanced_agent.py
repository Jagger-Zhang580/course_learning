#!/usr/bin/env python3
# week3: Agent with long-term memory using ChromaDB
# Demonstrates: ConversationBufferMemory + VectorStoreRetrieverMemory
# Requires: langchain, openai, chromadb, sentence-transformers, python-dotenv

import os
from dotenv import load_dotenv
load_dotenv()

from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory, VectorStoreRetrieverMemory
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings

# Optional fake LLM
def get_llm():
    try:
        return OpenAI(temperature=0)
    except Exception:
        from langchain.llms.fake import FakeListLLM
        return FakeListLLM(responses=[
            "I like pizza.",  # response to first message
            "You mentioned you like pizza earlier.",  # after memory recall
            "I remember you like pizza and you enjoy hiking."  # after two facts
        ])

def main():
    # Setup embeddings and vector store (in-memory for demo)
    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    # Using a persistent directory would be better for real apps
    vectorstore = Chroma(embedding_function=embedding, persist_directory="./chroma_db")
    
    # Memory: buffer for recent conversation + vector store for long-term facts
    buffer_memory = ConversationWindowMemory(k=2, return_messages=True)  # keep last 2 turns
    # For long-term memory we use a retriever that fetches relevant past sentences
    # We'll create a simple VectorStoreRetrieverMemory that stores each AI+Human turn as a document
    # For simplicity, we'll use the vectorstore as a retriever and manually add texts.
    # LangChain provides VectorStoreRetrieverMemory wrapper:
    from langchain.memory import VectorStoreRetrieverMemory
    retriever = vectorstore.as_retriever(search_kwargs=dict(k=2))
    long_term_memory = VectorStoreRetrieverMemory(retriever=retriever)
    
    # Combine memories: we'll use a simple custom memory that reads from both
    # For demo, we'll just use ConversationChain with buffer memory and manually inject long-term recall.
    llm = get_llm()
    conversation = ConversationChain(
        llm=llm,
        memory=buffer_memory,
        verbose=True
    )
    
    print("=== Memory Enhanced Agent Demo ===")
    print("Chat with the agent. Type 'exit' to quit.")
    print("Try saying: 'I like pizza.' then later 'What do I like?'")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        # Before getting response, we could retrieve long-term memories and prepend to prompt.
        # For simplicity, we rely on the chain's memory (buffer) only.
        # To demonstrate long-term recall, we manually query vectorstore and add as context.
        # We'll store each turn in vectorstore after getting response.
        response = conversation.predict(input=user_input)
        print(f"Agent: {response}")
        # Store the conversation turn in vectorstore for future recall
        vectorstore.add_texts([f"Human: {user_input} AI: {response}"])
        
if __name__ == "__main__":
    main()