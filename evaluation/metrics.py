from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

class AtlasEvaluator:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        # UPDATE: Using 'gemini-2.5-flash'
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )
        
        self.parser = JsonOutputParser()

        self.prompt = ChatPromptTemplate.from_template("""
        You are an AI Judge evaluating a RAG system.
        
        1. Faithfulness: Is the answer derived purely from the context? (0.0 to 1.0)
        2. Relevance: Does the answer directly address the user's question? (0.0 to 1.0)
        
        Question: {question}
        Answer: {answer}
        Context: {context}
        
        Return JSON only:
        {{
            "faithfulness": score,
            "relevance": score
        }}
        """)
        
        self.chain = self.prompt | self.llm | self.parser

    def evaluate(self, question, answer, context):
        """
        Evaluates the RAG response.
        """
        # print("⚖️  Atlas Judge is evaluating...") # Optional log
        try:
            trimmed_context = context[:3000] 
            scores = self.chain.invoke({
                "question": question,
                "answer": answer,
                "context": trimmed_context
            })
            return scores.get("faithfulness", 0), scores.get("relevance", 0)
            
        except Exception as e:
            # print(f"⚠️ Evaluation Error: {e}")
            return 0, 0