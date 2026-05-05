import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class QueryService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=self.api_key,
            temperature=0,
            max_retries=6
        )

    def expand_query(self, query: str) -> str:
        """Expand a simple query into a semantically rich set of search terms."""
        if len(query.split()) > 10: # Don't expand long, specific queries
            return query

        prompt = f"""
        You are a Semantic Query Expander. Your goal is to take a user's search query and expand it with a broad set of related concepts, synonyms, and technical terms.
        This is used for vector database retrieval, so the more diverse the related terms, the better.
        
        User Query: "{query}"
        
        Examples: 
        "money" -> "finance, budget, transaction, currency, payment, expenses, accounting, revenue"
        "security" -> "authentication, authorization, encryption, protection, firewall, login, vulnerability, hacking, safety"
        
        Response:
        Provide ONLY a comma-separated list of 10-15 expanded keywords and concepts.
        """
        
        try:
            response = self.llm.invoke(prompt)
            content = response.content
            if isinstance(content, list):
                content = " ".join([str(part) for part in content])
            return content.strip()
        except Exception:
            return query # Fallback to original query on failure
