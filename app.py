from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.rag_system import RAGSystem, generate_response
from src.quiz_agent import QuizAgent
from src.summary_tool import SummaryTool
from src.diagram_agent import DiagramAgent
from src.exam_guide_agent import ExamGuideAgent  # New import
import logging
import os
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize the RAG system
api_key = os.getenv("GOOGLE_API_KEY")  # Make sure this environment variable is set
pdf_path = "data/ncert_sound_chap.pdf"
rag_system = RAGSystem(api_key, pdf_path)

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
if not SARVAM_API_KEY:
    logger.error("SARVAM_API_KEY environment variable is not set")
    raise EnvironmentError("SARVAM_API_KEY environment variable is not set")

# Initialize ExamGuideAgent
exam_guide_agent = ExamGuideAgent(rag_system)

class Query(BaseModel):
    text: str

class QuizRequest(BaseModel):
    num_questions: int = 3

class DiagramRequest(BaseModel):
    diagram_type: str
    topic: str

class EvaluationRequest(BaseModel):
    question: str
    answer: str

class ExamGuideRequest(BaseModel):
    num_questions: int = 2

class TextToSpeechRequest(BaseModel):
    text: str
    target_language_code: str = "hi-IN"
    speaker: str = "meera"
    pitch: float = 0
    pace: float = 1.65
    loudness: float = 1.5
    speech_sample_rate: int = 8000
    enable_preprocessing: bool = True
    model: str = "bulbul:v1"

@app.post("/generate")
async def generate(query: Query):
    response = generate_response(query.text)
    return response

@app.post("/quiz")
async def generate_quiz(request: QuizRequest):
    quiz_agent = QuizAgent(rag_system)
    questions = quiz_agent.generate_questions(request.num_questions)
    return {"questions": questions}

@app.post("/evaluate_answer")
async def evaluate_answer(request: EvaluationRequest):
    quiz_agent = QuizAgent(rag_system)
    evaluation = quiz_agent.evaluate_answer(request.question, request.answer)
    return evaluation

@app.get("/chapter_summary")
async def get_chapter_summary():
    summary_tool = SummaryTool(rag_system)
    summary = summary_tool.generate_summary()
    return {"summary": summary}

@app.get("/important_topics")
async def get_important_topics():
    summary_tool = SummaryTool(rag_system)
    topics = summary_tool.generate_important_topics()
    return {"topics": topics}

@app.get("/summary_flowchart")
async def get_summary_flowchart():
    try:
        logger.info("Received request for chapter summary flowchart")
        diagram_agent = DiagramAgent(rag_system)
        flowchart = diagram_agent.generate_summary_flowchart()
        logger.info("Chapter summary flowchart generated successfully")
        return {"flowchart": flowchart}
    except Exception as e:
        logger.error(f"Error generating summary flowchart: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_exam_guide")
async def create_exam_guide(request: ExamGuideRequest):
    try:
        guide = exam_guide_agent.create_exam_guide(request.num_questions)
        return {"exam_guide": guide}
    except Exception as e:
        logger.error(f"Error creating exam guide: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/text_to_speech")
async def text_to_speech(request: TextToSpeechRequest):
    try:
        url = "https://api.sarvam.ai/text-to-speech"
        payload = {
            "inputs": [request.text],
            "target_language_code": request.target_language_code,
            "speaker": request.speaker,
            "pitch": request.pitch,
            "pace": request.pace,
            "loudness": request.loudness,
            "speech_sample_rate": request.speech_sample_rate,
            "enable_preprocessing": request.enable_preprocessing,
            "model": request.model
        }
        headers = {
            "Content-Type": "application/json",
            "API-Subscription-Key": SARVAM_API_KEY
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return {"audio_data": response.content}
    except requests.RequestException as e:
        logger.error(f"Error in text-to-speech conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Text-to-speech conversion failed: {str(e)}")


