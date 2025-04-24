# LangChain Agent API with LangGraph

Este projeto fornece um endpoint FastAPI para um agente conversacional construído usando Langchain e LangGraph. O agente pode conversar, usar ferramentas como busca na web (Tavily), e manter memória de conversação entre requisições.

## Estrutura do Projeto

```bash
agent_project/
│
├── app/                            # Código principal da aplicação
│   ├── __init__.py
│   ├── main.py                     # Entry point do FastAPI
│   ├── api/                        # Rotas e controladores
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── routes.py           # Endpoint /chat
│   │       └── schemas.py          # Pydantic models da API
│   │
│   ├── agents/                     # Lógica dos agentes LangGraph
│   │   ├── __init__.py
│   │   └── graph_agent.py          # Construtor do agente ReAct
│   │
│   ├── tools/                      # Ferramentas usadas pelos agentes
│   │   ├── __init__.py
│   │   ├── web_search_tool.py      # Ferramenta Tavily Search
│   │   └── vector_search_tool.py   # Placeholder para busca vetorial
│   │
│   ├── llm/                        # Setup dos modelos LLM
│   │   ├── __init__.py
│   │   └── openai_llm.py           # Configuração do LLM OpenAI
│   │
│   └── utils/                      # Utilitários (se necessário)
│       └── __init__.py
│
├── tests/                          # Testes (a implementar)
│   ├── __init__.py
│   ├── agents/
│   ├── api/
│   └── tools/
│
├── .env                            # Variáveis de ambiente (API Keys)
├── requirements.txt                # Dependências Python
└── README.md                       # Este arquivo
```

## Explicação do Fluxo de Funcionamento

Aqui está um passo a passo detalhado de como uma mensagem do usuário flui através do sistema:

1. **Usuário Envia Mensagem:**
    * Um usuário (ou sistema cliente) envia uma requisição HTTP POST para o endpoint `/api/v1/chat`.
    * O corpo da requisição inclui a mensagem (ex: `{"message": "Quem é o presidente do Brasil?"}`).
    * Crucialmente, um header `X-Session-Id` (ex: `"session-123"`) é incluído para identificar a conversa específica.

2. **FastAPI Recebe e Roteia:**
    * A aplicação FastAPI (`app/main.py`) recebe a requisição.
    * Ela roteia a requisição para a função `chat_endpoint` definida em `app/api/v1/routes.py`.

3. **Preparação no Endpoint (`chat_endpoint`):**
    * A mensagem do usuário é extraída do corpo da requisição.
    * O `X-Session-Id` é lido do header.
    * Um dicionário de configuração `config` para o LangGraph é criado, mapeando o ID da sessão para o `thread_id`: `{"configurable": {"thread_id": "session-123"}}`. Isso informa ao agente qual memória de conversa usar.
    * A mensagem do usuário é formatada na estrutura de entrada esperada pelo agente LangGraph: `{"messages": [HumanMessage(content="Quem é o presidente do Brasil?")]}`.

4. **Invocação do Agente LangGraph:**
    * A instância pré-construída do agente (`graph_agent_executor_instance` de `app/agents/graph_agent.py`) é invocada usando `ainvoke(input, config=config)`.
    * Esta instância foi criada usando `create_react_agent` do `langgraph.prebuilt`, que monta um grafo de agente seguindo o padrão ReAct (Reasoning and Acting).

5. **Dentro do Agente LangGraph (`create_react_agent`):**
    * **Carregar Estado:** O `MemorySaver` do agente (o `checkpointer` passado durante a criação) usa o `thread_id` da `config` para carregar o estado anterior (histórico de mensagens) desta sessão de conversa específica (`"session-123"`). Se for a primeira mensagem, o estado estará vazio.
    * **Loop ReAct:** O agente executa um ciclo de raciocínio e ação:
        * **Pensar (LLM):** O LLM configurado (`app/llm/openai_llm.py`) recebe o histórico atual de mensagens e a lista de ferramentas disponíveis (`TavilySearchResults`, `vector_search_placeholder` de `app/agents/graph_agent.py`). Ele decide a próxima ação. Para "Quem é o presidente do Brasil?", ele provavelmente decidirá usar a ferramenta de busca na web (Tavily).
        * **Agir (Chamada de Ferramenta):** O LLM gera uma "chamada de ferramenta" (Tool Call), especificando qual ferramenta usar (`tavily_search_results_json`) e os argumentos (`{"query": "Quem é o presidente do Brasil?"}`).
        * **Executar Ferramenta:** LangGraph intercepta a chamada, encontra a ferramenta `TavilySearchResults` correspondente e a executa com a query. A ferramenta (`app/tools/web_search_tool.py`) interage com a API do Tavily.
        * **Observar (Resultado da Ferramenta):** Os resultados da busca do Tavily são retornados ao grafo do agente.
        * **Pensar Novamente (LLM):** O resultado da ferramenta é adicionado ao histórico. O LLM recebe o histórico atualizado (UserInput -> LLM Thought/ToolCall -> Tool Result).
        * **Resposta Final (LLM):** Com base nos resultados da busca, o LLM formula a resposta final (ex: "O atual presidente do Brasil é Luiz Inácio Lula da Silva."). Como nenhuma outra ferramenta é necessária, ele gera a `AIMessage` final.
    * **Salvar Estado:** O `MemorySaver` (checkpointer) salva automaticamente o histórico completo e atualizado da conversa associado ao `thread_id` (`"session-123"`).

6. **Extração da Resposta no Endpoint:**
    * A chamada `ainvoke` na API retorna o dicionário completo do estado final do grafo (`final_state`).
    * A função `chat_endpoint` acessa a chave `'messages'` neste dicionário.
    * Ela recupera a *última* mensagem da lista, que é a `AIMessage` final do LLM.
    * O conteúdo textual (`.content`) desta `AIMessage` é extraído.

7. **Envio da Resposta ao Usuário:**
    * O texto extraído é empacotado em um objeto `ChatResponse`.
    * FastAPI serializa este objeto em JSON e o envia de volta como corpo da resposta HTTP para o usuário/cliente original.

## Como Rodar o Projeto

1. **Pré-requisitos:** Certifique-se de ter Python 3.11+ e `uv` (gerenciador de pacotes) instalados.

2. **Configuração Inicial (Ambiente e Dependências):**
    * **Windows:**
        * Execute o script `setup.bat`. Ele irá criar o ambiente virtual, ativá-lo e instalar as dependências do `requirements.txt` usando `uv`.

        ```bash
        setup.bat
        ```

        * Após a execução do script, o ambiente virtual (`.venv`) estará criado e pronto para uso.
    * **macOS/Linux (ou Manualmente no Windows):**
        * Crie o ambiente virtual: `uv venv` (ou `python -m venv .venv`)
        * Ative o ambiente:
            * Windows: `.venv\Scripts\activate`
            * macOS/Linux: `source .venv/bin/activate`
        * Instale as dependências: `uv pip install -r requirements.txt`

3. **Chaves de API:**
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Adicione suas chaves de API necessárias, como no exemplo:

        ```dotenv
        OPENAI_API_KEY=sua_chave_openai
        TAVILY_API_KEY=sua_chave_tavily
        # Adicione outras chaves se necessário (ex: Pinecone)
        ```

4. **Executar o Servidor:**
    * Certifique-se de que seu ambiente virtual está ativado.
    * Execute o servidor FastAPI usando Uvicorn:

        ```bash
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        ```

    * (Opcional) Se preferir usar o runner do `uv`:

        ```bash
        uv run fastapi dev app/main.py --host 0.0.0.0 --port 8000
        ```

        *(Nota: O comando `uv run fastapi dev` pode não passar argumentos como `--host` e `--port` corretamente para o Uvicorn subjacente em todas as versões/configurações. `uvicorn` direto é geralmente mais confiável para especificar host/port).*

5. **Testar:**
    * Acesse a documentação interativa da API (Swagger UI) no seu navegador em `http://localhost:8000/docs`.
    * Use a interface do Swagger ou uma ferramenta como `curl` ou Postman para enviar requisições POST para `http://localhost:8000/api/v1/chat`.
    * Inclua um corpo JSON como `{"message": "Sua pergunta aqui"}`.
    * **Importante:** Inclua o header `X-Session-Id: seu_id_de_sessao` para habilitar e rastrear a memória da conversa. Use o mesmo ID para continuar uma conversa existente.
