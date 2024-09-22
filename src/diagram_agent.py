# diagram_agent.py
from src.rag_system import RAGSystem
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiagramAgent:
    def __init__(self, rag_system: RAGSystem):
        self.rag_system = rag_system

    def generate_summary_flowchart(self) -> str:
        try:
            prompt = """
            Create a simple ASCII flowchart summarizing the key concepts of the Sound chapter.
            Use '-', '|', '+', and '>' for lines and arrows.
            Include all major topics at max 10 points, organized in a logical flow.
            """
            
            logger.info("Generating chapter summary flowchart")
            context = self.rag_system.vectorstore.similarity_search("Sound chapter summary", k=5)
            context_text = " ".join([doc.page_content for doc in context])
            
            ascii_flowchart = self.rag_system.get_gemini_response(context_text, prompt)
            logger.info("Chapter summary flowchart generated successfully")
            return ascii_flowchart
        except Exception as e:
            logger.error(f"Error generating flowchart: {str(e)}")
            return "Error: Unable to generate flowchart"