# exam_guide_agent.py

from typing import List
from src.rag_system import RAGSystem

class ExamGuideAgent:
    def __init__(self, rag_system: RAGSystem):
        self.rag_system = rag_system

    def create_exam_guide(self, num_questions: int = 2) -> str:
        prompt = f"""
        Generate an exam guide for the Sound chapter with {num_questions} important questions and their solutions.
        For each question:
        1. Provide a clear and concise question
        2. Provide a detailed solution that explains the concept and how to arrive at the answer
        3. Include any relevant formulas or equations
        4. Mention key points that are likely to earn marks in an exam

        Format your response as follows:
        Question 1: [Question text]
        Solution: [Detailed solution]

        Question 2: [Question text]
        Solution: [Detailed solution]

        ... and so on for {num_questions} questions.
        """

        context = self.rag_system.vectorstore.similarity_search("Sound chapter important concepts", k=10)
        context_text = " ".join([doc.page_content for doc in context])

        exam_guide = self.rag_system.get_gemini_response(context_text, prompt)
        return exam_guide