import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_community.callbacks import MlflowCallbackHandler

class Llm:
    """Wrapper class for llm model."""
    def __init__(self):
        load_dotenv(override=True)
        self._llm = None
        self._llm_32k = None

    def openai(self, model='gpt-4', callbacks=None):
        self._llm = ChatOpenAI(
                    model=model,#3.5-turbo',
                    api_key=os.getenv('OPENAI_KEY'),
                    temperature=0.7,
                    max_tokens=450,
                    verbose=True,
                    streaming=True,
                    callbacks=callbacks
                )
        
        return self._llm