from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Dict, Any, Optional

# Langchain/LangGraph imports
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage # Import message types
from langgraph.graph.graph import CompiledGraph # Type hint for agent executor

# App specific imports
from .schemas import ChatRequest, ChatResponse
from app.agents.graph_agent import graph_agent_executor_instance # Import the pre-built agent instance

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    # Use Header for session ID, default if not provided
    x_session_id: str = Header("default_session", description="Unique session identifier")
):
    """Handles chat requests using the LangGraph ReAct agent executor."""
    user_input = request.message
    # Config for LangGraph agent, associating the request with a thread_id
    config = {"configurable": {"thread_id": x_session_id}}
    
    response_text = "Agent encountered an issue." # Default error message

    print(f"Invoking agent for session: {x_session_id}")
    try:
        # Prepare input for the agent - expects a list of messages
        input_messages = [HumanMessage(content=user_input)]
        
        # Invoke the LangGraph agent executor
        # The checkpointer associated with the agent handles memory
        final_state = await graph_agent_executor_instance.ainvoke(
            {"messages": input_messages}, 
            config=config
        )

        # Extract the last message from the final state's message list
        if final_state and 'messages' in final_state and final_state['messages']:
            last_message: BaseMessage = final_state['messages'][-1]
            # Check if it's an AIMessage and extract content
            if isinstance(last_message, AIMessage) and hasattr(last_message, 'content'):
                response_text = last_message.content
            else:
                # Fallback if the last item isn't a standard AIMessage content
                response_text = str(last_message) 
                print(f"Warning: Last message type was {type(last_message)}")
        else:
             print("Warning: Agent finished but final state seems empty or missing messages.")
             response_text = "Agent process completed, but no response message found."

        print(f"Agent response for session {x_session_id}: {response_text}")
        return ChatResponse(response=response_text)

    except Exception as e:
        print(f"Error during LangGraph agent execution: {e}")
        import traceback
        traceback.print_exc()
        # Provide a more generic error to the user
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.") 