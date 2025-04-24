from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Dict, Any, Optional

from langchain.chains import LLMChain, ConversationChain
from langchain_core.language_models import BaseLanguageModel
from langchain.memory import ConversationBufferMemory

from .schemas import ChatRequest, ChatResponse
# Prompts & Parser
from app.prompts.router_prompt_template import ROUTER_PROMPT_TEMPLATE, RouterOutput, router_output_parser
from app.prompts.conversational_prompt import CONVERSATIONAL_PROMPT_TEMPLATE
# LLM
from app.llm.openai_llm import get_openai_llm
# Memory
from app.memory.session_memory import get_memory

router = APIRouter()

# --- Simple In-Memory Session Store (for demonstration) ---
# !! Not suitable for production - use Redis, DB, etc. !!
session_memory_store: Dict[str, ConversationBufferMemory] = {}

def get_session_memory(session_id: str) -> ConversationBufferMemory:
    """Gets or creates memory for a given session ID."""
    if session_id not in session_memory_store:
        # Create new memory if session doesn't exist
        session_memory_store[session_id] = get_memory(session_id)
        print(f"Created new memory for session: {session_id}")
    else:
        print(f"Reusing memory for session: {session_id}")
    return session_memory_store[session_id]
# -----------------------------------------------------------

# Dependency to get the LLM instance
def get_llm_dependency() -> BaseLanguageModel:
    return get_openai_llm()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    llm: BaseLanguageModel = Depends(get_llm_dependency),
    # Example: Get session ID from a header (replace with your session mechanism)
    x_session_id: Optional[str] = Header(None, description="Unique session identifier")
):
    """Handles chat requests with manual routing based on intent."""
    if not x_session_id:
        # Simple default if no session ID is provided (consider generating one)
        x_session_id = "default_session"
        
    user_input = request.message
    response_text = "Error: Could not determine route." # Default error

    try:
        # 1. Route the input
        # Create the routing chain (Prompt has PydanticOutputParser)
        router_llm_chain = LLMChain(llm=llm, prompt=ROUTER_PROMPT_TEMPLATE, verbose=True)
        
        # Invoke routing chain - result is likely {'text': 'JSON string'}
        raw_route_result = await router_llm_chain.ainvoke({"input": user_input})
        raw_output_text = raw_route_result.get("text", "{}") # Get raw JSON string
        
        # Manually parse the raw text output using the prompt's parser
        route_result: RouterOutput = router_output_parser.parse(raw_output_text)
        
        destination = route_result.destination
        print(f"Routing decision: {destination}")

        # 2. Execute the appropriate logic based on destination
        if destination == "conversa_geral":
            # Get or create memory for this session
            memory = get_session_memory(x_session_id)
            # Create conversational chain with memory
            conversation = ConversationChain(llm=llm, prompt=CONVERSATIONAL_PROMPT_TEMPLATE, memory=memory, verbose=True)
            # Run the chain
            result = await conversation.ainvoke(user_input) # Pass only input string
            response_text = result.get("response", "No conversational response.")

        elif destination == "pesquisa_internet":
            # Placeholder: Implement web search logic here
            # Example: web_search_tool.run(user_input)
            print(f"Placeholder: Executing web search for: {user_input}")
            response_text = f"Placeholder: Resultado da busca web para '{user_input}' iria aqui."
        
        elif destination == "consulta_vetores":
            # Placeholder: Implement vector store query logic here
            # Example: vector_store_retriever.get_relevant_documents(user_input)
            print(f"Placeholder: Executing vector query for: {user_input}")
            response_text = f"Placeholder: Resultado da consulta vetorial para '{user_input}' iria aqui."
        
        else:
            # Fallback if destination is unknown (shouldn't happen with good routing prompt)
            print(f"Warning: Unknown destination '{destination}'. Falling back to default.")
            # Let's fallback to conversation for safety
            memory = get_session_memory(x_session_id)
            conversation = ConversationChain(llm=llm, prompt=CONVERSATIONAL_PROMPT_TEMPLATE, memory=memory, verbose=True)
            result = await conversation.ainvoke(user_input)
            response_text = result.get("response", "No fallback response.")

        return ChatResponse(response=response_text)

    except Exception as e:
        print(f"Error during manual routing/execution: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred processing the request: {str(e)}") 