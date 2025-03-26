from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
import os
from dotenv import load_dotenv

load_dotenv()

class DadosdeEstudante(BaseTool):
  name = "Dados de Estudante"
  description = "Use essa ferramenta para obter os dados do estudante"

  def _run(self, nome_do_estudante: str):
    return f"O nome do estudante é {nome_do_estudante}"

pergunta = "Quais os dados da Ana?"

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"), temperature=0.5)

resposta = llm.invoke(pergunta)

print(resposta.content)


