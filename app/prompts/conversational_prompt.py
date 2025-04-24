from langchain.prompts import PromptTemplate

# Template para conversas gerais e amigáveis, com histórico
CONVERSATIONAL_PROMPT_TEMPLATE = PromptTemplate(
    template="""Você é um assistente amigável e conversador. Responda ao input do usuário de forma natural e acolhedora, levando em conta o histórico da conversa.

Histórico da Conversa:
{chat_history}

Input do Usuário: {input}
Sua Resposta Amigável:""",
    input_variables=["chat_history", "input"],
) 