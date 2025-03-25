from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


numero_de_dias = 7
numero_de_criancas = 2
atividade = "praia"

modelo_do_prompt = PromptTemplate.from_template( 
  "Crie um roteiro de viagem de {numero_de_dias} dias, para uma família com {numero_de_criancas} crianças, que gostam de {atividade}."

)

prompt = modelo_do_prompt.format(numero_de_dias=numero_de_dias, numero_de_criancas=numero_de_criancas, atividade=atividade)

print(prompt)

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key="", temperature=0.5)

resposta = llm.invoke(prompt)

print(resposta)

roteiro_viagem = resposta.choices[0].message.content
print(roteiro_viagem.content)
