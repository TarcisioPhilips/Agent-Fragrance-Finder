from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor

# Import necessary components from other modules
from app.llm.openai_llm import get_openai_llm
from app.tools.web_search_tool import get_tavily_search_tool

def get_agent_executor():
    """Creates and returns the LangChain agent executor."""
    llm = get_openai_llm()
    
    # Define tools - currently just Tavily Search
    # In the future, you might load multiple tools dynamically
    tools = [get_tavily_search_tool(max_results=1)]
    
    # Get the ReAct prompt
    # Consider moving the prompt pulling/definition to app/prompts
    prompt = hub.pull("hwchase17/react")
    
    # Create the Agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Create the Agent Executor
    # Set verbose=False for production environments
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

# Optional: You can create a single instance for reuse if needed
# agent_executor_instance = get_agent_executor() 