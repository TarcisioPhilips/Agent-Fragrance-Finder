import os
from langchain_openai import ChatOpenAI

def get_openai_llm():
    """Initializes and returns the ChatOpenAI LLM instance."""
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    # Consider adding more configuration options here (temperature, etc.)
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    return llm 