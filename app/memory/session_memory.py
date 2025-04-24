from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage
from typing import List, Sequence # Added for type hints

# Nota: Para memória persistente entre requisições,
# seria necessário um backend de armazenamento (ex: Redis, DB)
# e um mecanismo para associar a memória a um ID de sessão.
# Esta implementação simples cria uma nova memória a cada chamada.

def get_memory(session_id: str = "default") -> ConversationBufferMemory:
    """Retorna uma instância de ConversationBufferMemory.
    
    Args:
        session_id (str): Um identificador para a sessão (atualmente não usado 
                          para armazenamento persistente, mas pode ser útil no futuro).

    Returns:
        ConversationBufferMemory: Instância da memória.
    """
    # Aqui você poderia implementar a lógica para carregar/salvar
    # o histórico de um armazenamento externo baseado no session_id.
    # Por agora, apenas cria uma memória em branco.
    return ConversationBufferMemory(
        memory_key="chat_history", 
        input_key="input", # Garante que o input seja adicionado corretamente
        return_messages=True
    )

# Exemplo (opcional) de como poderia ser um armazenamento simples em memória (não recomendado para produção)
# message_history_store: Dict[str, BaseChatMessageHistory] = {}
# def get_persistent_memory(session_id: str) -> ConversationBufferMemory:
#     if session_id not in message_history_store:
#         message_history_store[session_id] = ChatMessageHistory()
#     return ConversationBufferMemory(
#         chat_memory=message_history_store[session_id],
#         memory_key="chat_history", 
#         input_key="input", 
#         return_messages=True
#     ) 