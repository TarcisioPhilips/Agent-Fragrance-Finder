from typing import Sequence

from langchain_core.language_models import BaseLanguageModel
from langchain_core.tools import BaseTool
from langgraph.checkpoint.memory import MemorySaver # Import MemorySaver
from langgraph.prebuilt import create_react_agent # Import the agent factory
from langgraph.graph.graph import CompiledGraph # For type hinting

# Import LLM and Tools
from app.llm.openai_llm import get_openai_llm
from app.tools.web_search_tool import get_tavily_search_tool
from app.tools.vector_search_tool import vector_search_placeholder

# --- Agent Configuration ---

# Instantiate tools
# O Agente decidirá qual usar com base na descrição delas
tools: Sequence[BaseTool] = [
    get_tavily_search_tool(max_results=3),
    vector_search_placeholder,
]

# Instantiate Memory Checkpointer (singleton at module level for simplicity)
# Em produção, gerencie checkpointers de forma mais robusta (ex: por sessão)
checkpointer = MemorySaver()

def build_graph_agent_executor() -> CompiledGraph:
    """Builds the LangGraph ReAct agent executor."""
    print("Building LangGraph agent executor...")
    llm = get_openai_llm()
    
    # Create the ReAct agent graph using the prebuilt function
    # Pass the llm, tools, and the checkpointer for memory
    agent_executor = create_react_agent(
        llm, 
        tools, 
        checkpointer=checkpointer
    )
    print("LangGraph agent executor built.")
    return agent_executor

# --- Optional: Create a single instance for the API to use ---
# This avoids rebuilding the graph structure on every request
# (though state is still managed per thread_id by the checkpointer)
graph_agent_executor_instance: CompiledGraph = build_graph_agent_executor() 