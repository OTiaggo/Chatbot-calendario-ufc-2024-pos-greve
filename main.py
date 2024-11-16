from dotenv import load_dotenv
import os
load_dotenv()  

import asyncio
from langchain_openai import ChatOpenAI
from typing import List
from langchain_core.documents import Document
from langchain_unstructured import UnstructuredLoader
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Qdrant
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.schema import HumanMessage

#Carregar modelo
model = ChatOpenAI(model_name="gpt-4o-mini")

#Carregar páginas web
async def _get_setup_docs_from_url(url: str) -> List[Document]:
  loader = WebBaseLoader(web_paths=[url])
  docs = []
  async for doc in loader.alazy_load():
    docs.append(doc)

  return docs

page_urls = [
    "https://www.ufc.br/calendario-universitario/2024-ajuste-pos-greve",
    "https://www.ufc.br/noticias/18775-entenda-a-retomada-das-atividades-na-ufc-e-confira-as-principais-datas-do-novo-calendario-academico",
]

documents = []
async def funcao_assincrona(url):
    return await _get_setup_docs_from_url(url)
    
for url in page_urls:
  page_setup_docs = asyncio.run(funcao_assincrona(url))
  documents.extend(page_setup_docs)
  

#Criando embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

qdrant = Qdrant.from_documents(
    documents=[documents[0], documents[1]],
    embedding=embeddings,
    location=":memory:",
    collection_name="chatbot"
)

#Criando prompt
def custom_prompt(query: str):
  results = qdrant.similarity_search(query, k=3)
  source_knowledge = "\n".join([r.page_content for r in results])
  augmented_prompt = f"""Use o contexto abaixo para responder à pergunta relacionado às datas da Universidade Federal do Ceará(UFC).
  Contexto:
  {source_knowledge}
  Pergunta: {query}"""
  return augmented_prompt