import sys

sys.path.append('')
from src.backend.SQL_db import PostGresDB
from src.backend.embed_datasets import DatasetEmbedding
from src.backend.llm import Llm
from src.backend.scraper import extract_content
#from src.backend.scrap_web import extract_content
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

import logging

logging.basicConfig(level=logging.INFO)

class KeywordsGenerator:

    def __init__(self):
        self.llm = Llm().openai(model='gpt-4-turbo')
        self.embed_DB = DatasetEmbedding()
        self.post_DB = PostGresDB()
        self.post_DB.connect()

    def keywords_from_dataset(self, url: str):
        prompt_template = """Task: Transform the content of a Gaia-X website presenting a data service into a concise list of keywords only related to that data service, ignoring the trash and avoid .

                    Objective: Generate a concise list of relevant keywords that accurately represent the core topics only of the data service ignoring the trash in between.

                    Example:

                    Text: "Owned by 0xd1E0…C3f0Accessed with SEMCO-1 computealgorithmPublished 9 months agoThis data service contains the import functionality of the semantic collaboration service for the exchange of descriptive models and analytics.
The semantic collaboration service supports on the one hand descriptive models (e.g., architecture or design models), to store data series on a grid (time, frequency). It can then be used to access analysis or test results, technical test results, technical budgets (e.g. mass, power consumption, ...) or performance indicators in the dashboard.
The distributed work of different organizations in space projects can be greatly simplified by GAIA-X. The goal of semantic collaboration service is to enable semantic continuity between different organizations. Semantic continuity is the ability to exchange data between different applications,  project phases and organizations in a way that the meaning of the data is preserved.
Test Disclaimer
This is in no way a real or binding offering, but just serving illustration and development purposes.
Data Authoritemis AGOwner0xd1E0…C3f0Docker Imagedeltadao/semanticcollaboration:v1.0.0DIDdid:op:739b2e3158ccd6db1b47ca5d84a63ba258732c70dcdcc7ae519ac57bb1c37e6dMetadata HistoryNFT metadata updated 8 months ago NFT metadata updated 9 months ago published 9 months ago" 
                    
                    Keywords: ['Descriptive Models', 'Semantic', 'Data Series', 'Power Consumption', 'Space']

                    Instructions:

                    1. Read the text
                    2. Generate Keywords: Extract key themes and concepts from of the dataset.
                    3. Create a list of relevant keywords and return it in the following json format {{'keywords': ['keyword1', ...]}}.

                    Let's Begin!

                    Data: {metadata}
                    Keywords:
        """
        
        prompt = PromptTemplate.from_template(prompt_template)

        chain = prompt | self.llm | JsonOutputParser()

        metadata = self.get_html(url)
        logging.info(f"Extracted metadata: {metadata}")
        try:
            ans = chain.invoke({'metadata': metadata})
            return ans['keywords']
        except Exception as e:
            return []


    def send_to_databases(self, url: str, id:str, vc_id: str, title: str):
        keywords = self.keywords_from_dataset(url)
        self.send_to_milvus(keywords, id, vc_id)
        self.send_to_postgres(keywords, id, title)

    def send_to_postgres(self, keywords: list, id: str, title: str):
        formatted_str = "{" + ",".join(f"{item}" for item in keywords) + "}"
        logging.info(f"Inserting data into Postgres DB: {formatted_str}")
        self.post_DB.insert_data([(id, formatted_str, title)])
    
    def send_to_milvus(self, keywords, id: str, vc_id: str):
        logging.info(f"Inserting data into Milvus DB: {keywords}")
        for keyword in keywords:
            self.embed_DB.add_text(keyword, metadata={'id': id, 'vc_id': vc_id})

    def get_html(self, url: str):
        return extract_content(url, {'extraction_type': 'scraper'})