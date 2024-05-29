import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings

class Embedding:
    """Wrapper class for embedding model"""
    def __init__(self):
        load_dotenv()
        self._embedding = None

    def openai(self, model='text-embedding-ada-002'):
        openai_key = os.getenv('OPENAI_KEY')
        
        assert openai_key is not None, "OpenAI key not provided."
        
        if self._embedding is None:
            self._embedding = OpenAIEmbeddings(
                api_key=openai_key,
                model=model
            )
        return self._embedding