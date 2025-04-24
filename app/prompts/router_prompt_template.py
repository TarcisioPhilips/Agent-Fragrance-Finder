from langchain.prompts import PromptTemplate
# Re-import Pydantic parser and helpers
from langchain.output_parsers import PydanticOutputParser 
from pydantic import BaseModel, Field
from typing import Dict

# --- Modelo Pydantic para a saída JSON do Roteador ---
class RouterOutput(BaseModel):
    destination: str = Field(description="O nome da rota para onde direcionar o input do usuário (ex: 'pesquisa_internet', 'consulta_vetores', 'conversa_geral').")
    # Ensure next_inputs includes the original input
    next_inputs: Dict[str, str] = Field(description="Um dicionário contendo o input original do usuário sob a chave 'input'.")

# --- Parser para a saída JSON do Roteador ---
router_output_parser = PydanticOutputParser(pydantic_object=RouterOutput)

# --- Template do Prompt Atualizado para pedir JSON ---
ROUTER_PROMPT_TEMPLATE_TEXT = """Dado o input do usuário abaixo, classifique-o como apropriado para uma das seguintes opções:
'pesquisa_internet' - Para perguntas gerais que exigem busca na web (notícias, fatos, etc.).
'consulta_vetores' - Para perguntas sobre informações específicas contidas em documentos ou base de conhecimento interna.
'conversa_geral' - Para saudações, conversas informais, perguntas pessoais ou comandos que não se encaixam nas outras categorias.

Retorne um objeto JSON formatado de acordo com as instruções abaixo. Garanta que o campo 'next_inputs' contenha o input original do usuário.

{format_instructions}

<< INPUT DO USUÁRIO >>
{input}

<< SAÍDA JSON >>""" # Prompt agora pede JSON

ROUTER_PROMPT_TEMPLATE = PromptTemplate(
    template=ROUTER_PROMPT_TEMPLATE_TEXT,
    input_variables=["input"],
    # Add partial variables for format instructions
    partial_variables={"format_instructions": router_output_parser.get_format_instructions()}, 
    # Attach the PydanticOutputParser directly to the prompt
    output_parser=router_output_parser, 
) 