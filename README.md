# NCERT Sound Chapter Interactive Learning Tools

This project provides an interactive learning platform for the NCERT Sound chapter, offering various tools to enhance understanding and engagement with the material.

A detailed development guide can be found on [notion]([https://colab.research.google.com/drive/1jeRa0pO2V_ZaGVyVIVg-CkoLWxENhUcg?usp=sharing](https://sugared-zoo-169.notion.site/Sarvam-AI-RAG-1095f7d84122802e9834f475a9fde624?pvs=74))

## Features

1. **Question & Answer System**: Ask questions about the Sound chapter and receive detailed answers.
2. **Text-to-Speech**: Convert text answers to speech for auditory learning.
3. **Chapter Summary**: Generate concise summaries of the chapter content.
4. **Interactive Quiz**: Take quizzes with dynamically generated questions and receive instant feedback.
5. **Summary Flowchart**: Visualize the chapter's key concepts in a flowchart format.
6. **Exam Guide**: Generate custom exam guides with practice questions.

## Technology Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **AI Model**: Google's Gemini 1.5 Flash
- **Vector Database**: Chroma
- **Embeddings**: Hugging Face (sentence-transformers/all-MiniLM-L6-v2)
- **PDF Processing**: PyPDFLoader, PDFPlumberLoader
- **Text-to-Speech**: Sarvam AI API

## Project Structure

- `api.py`: FastAPI backend server
- `frontend.py`: Streamlit frontend application
- `ingest.py`: PDF ingestion and text splitting
- `rag_system.py`: RAG (Retrieval-Augmented Generation) system implementation
- `vector_db.py`: Vector database creation and management

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install fastapi streamlit langchain google-generativeai requests chromadb sentence_transformers langchain_community pydantic chromadb  uvicorn
   ```
3. Set up environment variables:
   - `GOOGLE_API_KEY`: Your Google API key for Gemini
   - `SARVAM_API_KEY`: Your Sarvam AI API key for text-to-speech

## Running the Application

1. Start the FastAPI backend:
   ```
   uvicorn api:app --reload
   ```
2. Run the Streamlit frontend:
   ```
   streamlit run frontend.py
   ```

## Usage

1. Open the Streamlit app in your browser (typically at `http://localhost:8501`).
2. Use the sidebar to navigate between different tools:
   - Ask questions about the Sound chapter
   - Generate chapter summaries
   - Take quizzes
   - View summary flowcharts
   - Create exam guides
3. Explore the Text-to-Speech feature to listen to responses.
