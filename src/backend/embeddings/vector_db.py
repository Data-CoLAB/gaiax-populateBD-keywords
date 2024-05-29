from langchain_community.vectorstores import Milvus
from dotenv import load_dotenv
import os

class Vector_DB():
    def __init__(self):
        load_dotenv()

        MIVLUS_URI = os.getenv("ENDPOINT_MILVUS")
        MILVUS_API_KEY = os.getenv("MILVUS_KEY")

        MILVUS_HOST = os.getenv("MILVUS_HOST")
        MILVUS_PORT = os.getenv("MILVUS_PORT")

        if MIVLUS_URI is not None and MILVUS_API_KEY is not None:
            self._conn_args = {
                "uri": MIVLUS_URI,
                "token": MILVUS_API_KEY,
                "secure": True,
            }
        elif MILVUS_HOST is not None and MILVUS_PORT is not None:
            self._conn_args = {
                "host": MILVUS_HOST,
                "port": MILVUS_PORT,
            }
        else:
            raise ValueError("Milvus connection details not provided.")

    def retrieve(self, embedding, collection='cit') -> Milvus:
        """
        Retrieve a Milvus vector store instance.

        Parameters:
        - embedding (OpenAIEmbeddings): The embedding model to use.
        - collection (str): The name of the collection to retrieve.

        Returns:
        - vector_db: An instance of Milvus vector store.
        """
        vector_db = Milvus(
            embedding,
            connection_args=self._conn_args,
            collection_name=collection,
            auto_id=True
        )
        return vector_db
    
    def doc_store(self, docs, embedding, collection='cit'):
        vector_db = Milvus.from_documents(
            docs,
            embedding,
            connection_args=self._conn_args,
            collection_name=collection
        )
        return vector_db

    def from_texts(self, texts, embedding, collection='cit'):
        vector_db = Milvus.from_texts(
            texts,
            embedding,
            connection_args=self._conn_args,
            collection_name=collection
        )
        return vector_db
    
    def add_texts(self, vector_db, texts, metadatas):
        vector_db.add_texts(texts, metadatas=metadatas)