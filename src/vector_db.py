# vector_db.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

def create_vector_store(texts, persist_directory='db'):
    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        # Ensure the persist directory exists
        os.makedirs(persist_directory, exist_ok=True)
        
        vectorstore = Chroma.from_documents(
            documents=texts, 
            embedding=embeddings, 
            persist_directory=persist_directory
        )
        
        # Persist the vectorstore
        vectorstore.persist()
        
        print(f"Vector store created successfully with {len(texts)} documents.")
        return vectorstore
    except Exception as e:
        print(f"Error creating vector store: {str(e)}")
        return None