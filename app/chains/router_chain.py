from typing import Dict
from langchain.chains import LLMChain, ConversationChain
from langchain.chains.router import MultiPromptChain
# Import LLMRouterChain constructor directly and the parser
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import PromptTemplate # Usado para placeholders e conversa

# Import dos prompts
from app.prompts.router_prompt_template import ROUTER_PROMPT_TEMPLATE
from app.prompts.conversational_prompt import CONVERSATIONAL_PROMPT_TEMPLATE

# Import da função de memória
from app.memory.session_memory import get_memory 

# --- Placeholders para as chains de destino --- 
# TODO: Substitua por imports reais quando as chains forem implementadas
# from app.tools.web_search_tool import web_search_chain 
# from app.tools.pinecone_query_tool import pinecone_tool_chain

# --- Função helper para criar chains (mantida para placeholders) ---
def _create_placeholder_chain(llm: BaseLanguageModel, name: str) -> LLMChain:
    """Cria uma chain placeholder simples (usada para rotas não implementadas)."""
    prompt = PromptTemplate(
        template=f"Placeholder: {name}. Input: {{input}}",
        input_variables=["input"]
    )
    return LLMChain(llm=llm, prompt=prompt, verbose=False) # Less verbose placeholders

# --- Função principal para construir a MultiPromptChain ---
def build_router_chain(llm: BaseLanguageModel) -> MultiPromptChain:
    """Constrói e retorna a MultiPromptChain para roteamento (abordagem manual)."""

    # Chains de Destino
    web_search_chain = _create_placeholder_chain(llm, "pesquisa_internet")
    pinecone_tool_chain = _create_placeholder_chain(llm, "consulta_vetores")
    conversational_memory = get_memory()
    conversational_chain = ConversationChain(
        llm=llm,
        prompt=CONVERSATIONAL_PROMPT_TEMPLATE,
        memory=conversational_memory,
        verbose=True
    )
    destination_chains: Dict[str, LLMChain] = {
        "pesquisa_internet": web_search_chain,
        "consulta_vetores": pinecone_tool_chain,
        "conversa_geral": conversational_chain,
    }
    default_chain = conversational_chain

    # --- Construção Manual do Router ---
    # 1. LLMChain base usando o prompt que já tem o PydanticOutputParser
    base_router_llm_chain = LLMChain(
        llm=llm,
        prompt=ROUTER_PROMPT_TEMPLATE,
        verbose=True
    )

    # 2. LLMRouterChain usando o construtor direto
    # A base_router_llm_chain já tem o parser Pydantic anexado ao prompt.
    router_chain = LLMRouterChain(
        llm_chain=base_router_llm_chain, 
        # output_parser=RouterOutputParser(), # Removido - Deixando o parser do prompt fazer o trabalho
    )
    # -------------------------------------

    # Criação da MultiPromptChain final
    multi_prompt_chain = MultiPromptChain(
        router_chain=router_chain,
        destination_chains=destination_chains,
        default_chain=default_chain,
        verbose=True,
    )

    return multi_prompt_chain 