# summary_tool.py

from src.rag_system import RAGSystem

class SummaryTool:
    def __init__(self, rag_system: RAGSystem):
        self.rag_system = rag_system

    def generate_summary(self) -> str:
        prompt = """
        Generate a concise summary of the most important points in the Sound chapter. Try to cover the experiments and important question additionally.
        The summary should:
        1. Cover the main concepts and principles
        2. Highlight key experiments or demonstrations
        3. Mention any important formulas or equations
        4. Be easy to understand for a high school student
        5. Be organized with bullet points or numbered list for clarity
        """
        
        context = self.rag_system.vectorstore.similarity_search(prompt, k=10)
        context_text = " ".join([doc.page_content for doc in context])
        
        summary = self.rag_system.get_gemini_response(context_text, prompt)
        return summary

    def generate_important_topics(self) -> str:
        prompt = """
        Generate a list of important topics covered in the Sound chapter of the NCERT book. The list should be in form of a flow chart made with symbols.
        The list should:
        1. Include major concepts and principles related to sound
        2. Cover key phenomena and their explanations
        3. Include any significant experiments or applications discussed
        4. Be organized as a bulleted list
        5. Provide a brief (1-2 sentence) explanation for each topic at the end of flow chart.
        """

        context = self.rag_system.vectorstore.similarity_search(prompt, k=10)
        context_text = " ".join([doc.page_content for doc in context])

        topics = self.rag_system.get_gemini_response(context_text, prompt)
        return topics