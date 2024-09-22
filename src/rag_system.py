# rag_system.py
import os
import google.generativeai as genai
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.ingest import load_and_split_documents
import logging

logging.basicConfig(level=logging.INFO)

class RAGSystem:
    def __init__(self, api_key, pdf_path):
        self.configure_genai(api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.vectorstore = self.initialize_vectorstore(pdf_path)

    @staticmethod
    def configure_genai(api_key):
        os.environ["GOOGLE_API_KEY"] = api_key
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    @staticmethod
    def initialize_vectorstore(pdf_path):
        texts = load_and_split_documents(pdf_path)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(texts, embeddings, persist_directory='db')
        logging.info(f"Vector store initialized with {len(texts)} documents.")
        return vectorstore

    def get_gemini_response(self, context, query):
        try:
            response = self.model.generate_content(f""" 
            Using the context given below answer the query.                             
            CONTEXT: {context}
            QUERY: {query}   
            Give answers to point and easy to understand with good formatting.                            
            """)
            return response.text
        except Exception as e:
            logging.error(f"Error generating Gemini response: {str(e)}")
            return "I'm sorry, but I encountered an error while processing your request."

    def generate_response(self, query):
        try:
            retrieved_documents = self.vectorstore.similarity_search(query, k=5)
            context = " ".join([doc.page_content for doc in retrieved_documents])
            
            result = self.get_gemini_response(context, query)
            
            return {"result": result, "source": context}
        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            return {"result": "I'm sorry, but I encountered an error while processing your request.", "source": ""}

# Initialize the RAG system
api_key = os.getenv("GOOGLE_API_KEY")  # Make sure this environment variable is set
pdf_path = "data/ncert_sound_chap.pdf"  # Ensure this path is correct

rag_system = None
try:
    rag_system = RAGSystem(api_key, pdf_path)
except Exception as e:
    logging.error(f"Failed to initialize RAG system: {str(e)}")

# Function to be called by the API
def generate_response(query):
    if rag_system:
        return rag_system.generate_response(query)
    else:
        return {"result": "RAG system is not initialized properly.", "source": ""}