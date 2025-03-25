from langchain_openai import ChatOpenAI

numero_de_dias = 7
numero_de_criancas = 2
atividade = "praia"

prompt = f"Crie um roteiro de viagem de {numero_de_dias} dias, para uma família com {numero_de_criancas} crianças, que gostam de {atividade}."
print(prompt)

llm = ChatOpenAI(model="gpt-3.5-turbo", api_key="", temperature=0.5)

resposta = llm.invoke(prompt)

print(resposta)

roteiro_viagem = resposta.choices[0].message.content
print(roteiro_viagem.content)
