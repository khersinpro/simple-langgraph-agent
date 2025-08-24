import os
from langchain_openai import ChatOpenAI

class OpenAIFactory:
    @staticmethod
    def create_llm(model: str = "gpt-5-nano", temperature: float = 0) -> ChatOpenAI:
        """
        Creates and configures a ChatOpenAI instance.
        Values are taken from environment variables if not specified.
        """
        api_key = os.getenv("OPEN_API_KEY")

        if not api_key:
            raise ValueError("OPEN_API_KEY environment variable is not defined or .env file has not been loaded.")

        print(f"Creating LLM with model {model} and API key.")
        
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key
        )