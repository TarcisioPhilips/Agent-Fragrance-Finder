import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor

# Load environment variables
load_dotenv()

# --- FastAPI Setup ---
app = FastAPI(
    title="LangChain Agent API",
    description="API endpoint for a LangChain agent.",
    version="0.1.0",
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# --- LangChain Agent Setup ---

# Ensure API keys are set (example uses OpenAI and Tavily)
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable not set.")
if not os.getenv("TAVILY_API_KEY"):
    raise ValueError("TAVILY_API_KEY environment variable not set.")

# 1. Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 2. Define Tools
tools = [TavilySearchResults(max_results=1)]

# 3. Get the ReAct prompt
prompt = hub.pull("hwchase17/react")

# 4. Create the Agent
agent = create_react_agent(llm, tools, prompt)

# 5. Create the Agent Executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # Set verbose=False for production


# --- API Endpoint ---
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Receives a message and returns the agent's response."""
    try:
        # Use invoke for synchronous execution suitable for FastAPI request/response
        result = agent_executor.invoke({"input": request.message})
        return ChatResponse(response=result.get("output", "No output found."))
    except Exception as e:
        # Basic error handling
        return ChatResponse(response=f"An error occurred: {str(e)}")

# --- Run instruction (for local development) ---
# To run this app: uvicorn main:app --reload

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 