import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from app.llm.openai_llm import get_openai_llm

QUERY_PROMPT = """Convert the user request into an effective e-commerce search query.
Focus on finding actual products for sale with prices, not articles or reviews.

Rules:
- Include specific e-commerce sites: site:amazon.com OR site:sephora.com OR site:mercadolivre.com.br
- Add "price" and "buy now" to focus on product listings with prices
- Exclude words like "review", "article", "blog", "best of"
- Add "in stock" to find available products

User Request: {user_request}

Search Query:"""

FORMAT_PROMPT = """Format the search results as a list of actual products for sale.
Only include products with real prices and valid e-commerce URLs.

Format:
1. [Product Name]: [Price] ([Product URL])
2. [Product Name]: [Price] ([Product URL])
3. [Product Name]: [Price] ([Product URL])

Rules:
- Only include actual product listings from e-commerce sites
- Exclude blog posts, articles, or review pages
- If price is not available, use 'Price not available'
- If URL is not available, use 'No URL available'
- If no valid products found, return: "Nenhum produto encontrado para a especificação. Tente refinar sua busca."

Search Results:
{search_results}

Formatted Response:"""

def get_tavily_search_tool(max_results: int = 5):
    """Initializes and returns the TavilySearchResults tool with LLM formatting."""
    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY environment variable not set.")
    
    base_tool = TavilySearchResults(max_results=max_results)
    llm = get_openai_llm()
    query_prompt = ChatPromptTemplate.from_template(QUERY_PROMPT)
    format_prompt = ChatPromptTemplate.from_template(FORMAT_PROMPT)
    
    def formatted_search(query: str) -> str:
        """Searches the web and formats results with product name, price and URL."""
        try:
            # Optimize the query first
            optimized_query = llm.invoke(query_prompt.invoke({"user_request": query})).content
            print(f"Optimized Query: {optimized_query}")
            
            # Use optimized query for search
            raw_results = base_tool.invoke(optimized_query)
            print(f"Raw Results: {raw_results}")
            
            # Format results
            formatted = format_prompt.invoke({"search_results": str(raw_results)})
            result = llm.invoke(formatted).content
            
            # Check if no valid products were found
            if "Nenhum produto encontrado" in result:
                return result
                
            return result
        except Exception as e:
            return f"Error performing search: {str(e)}"
    
    return formatted_search 