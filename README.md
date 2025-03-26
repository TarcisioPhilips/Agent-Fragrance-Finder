# Agente de orientação acadêmica

## 🔨 Funcionalidades do projeto

Neste projeto desenvolvemos um conjunto de assistentes que permitem auxiliar no processo de identificação de universidades para perfis específicos de estudantes. Para isso, implementamos uma solução em Python, utilizando LangChain e a LLM da OpenAI. Nesta abordagem, criamos um conjunto de agentes para (i) recuperar dados do usuário (ii) gerar um perfil do usuário e (iii) identificar universidades que combinam com este perfil. Além disso, implementamos um hub par agestão dos agentes e ferramentas criadas.

## ✔️ Técnicas e tecnologias utilizadas

As técnicas e tecnologias utilizadas pra isso são:

- Programação Orientada à Objetos em Python
- Uso de API GPT OpenAI
- Uso de cadeias, com LangChain
- Uso de agentes OpenAI
- Uso de Agentes ReAct
- Leitura de arquivos CSV e manipulação de dados

## 🛠️ Abrir e rodar o projeto

Após baixar o projeto, você pode abrir com Visual Studio Code. Em seguida, é necessário que você prepare seu ambiente. Para isso:

### venv no Windows

```bash
python -m venv agent-poc
agent-poc\Scripts\activate
```

### venv no Mac/Linux

```bash
python3 -m venv agent-poc
source agent-poc/bin/activate
```

Em seguida, instale os pacotes utilizando:

```bash
pip install -r requirements.txt
```

## 🔑 Gerar API_KEY e associar ao .env

```python
OPENAI_API_KEY = "SUA_CHAVE_AQUI"
```
