import os
from langchain_community.tools.tavily_search import TavilySearchResults

def get_tavily_search_tool(max_results: int = 1):
    """Initializes and returns the TavilySearchResults tool."""
    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY environment variable not set.")
    tool = TavilySearchResults(max_results=max_results)
    return tool 