# quiz_agent.py

import random
from typing import List, Dict
from src.rag_system import RAGSystem

class QuizAgent:
    def __init__(self, rag_system: RAGSystem):
        self.rag_system = rag_system

    def generate_questions(self, num_questions: int = 3) -> List[str]:
        question_prompts = [
            "Generate a multiple-choice question about",
            "Create a true/false question related to",
            "Formulate a fill-in-the-blank question concerning",
            "Devise a short answer question about",
        ]
        
        questions = []
        for _ in range(num_questions):
            topic = self.rag_system.vectorstore.similarity_search("Generate a random topic from the sound chapter", k=2)[0].page_content
            prompt = random.choice(question_prompts)
            question = self.rag_system.get_gemini_response(topic, f"{prompt} {topic}")
            questions.append(question)
        
        return questions

    def evaluate_answer(self, question: str, user_answer: str) -> Dict[str, str]:
        prompt = f"""
        Question: {question}
        User's Answer: {user_answer}
        
        Evaluate if the user's answer is correct. If it's not entirely correct, provide a brief explanation of the correct answer.
        Return your response in the following format:
        Correct: [True/False]
        Explanation: [Your explanation if the answer is incorrect, or 'Great job!' if correct]
        """
        evaluation = self.rag_system.get_gemini_response("", prompt)
        return {"evaluation": evaluation}