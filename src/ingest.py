# ingest.py
from langchain_community.document_loaders import PyPDFLoader, PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging

logging.basicConfig(level=logging.INFO)

def load_and_split_documents(pdf_path):
    # Try PyPDFLoader first
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    if not documents:
        # If PyPDFLoader fails, try PDFPlumberLoader
        loader = PDFPlumberLoader(pdf_path)
        documents = loader.load()
    
    logging.info(f"Loaded {len(documents)} pages from the PDF")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
        length_function=len
    )
    texts = text_splitter.split_documents(documents)
    
    logging.info(f"Split into {len(texts)} text chunks")
    
    return texts

# # Add this if you want to test the function directly
# if __name__ == "__main__":
#     pdf_path = "data/ncert_sound_chap.pdf"  
#     texts = load_and_split_documents(pdf_path)
#     print(f"Total chunks: {len(texts)}")
#     print(f"First chunk preview: {texts[0].page_content[:100]}...")