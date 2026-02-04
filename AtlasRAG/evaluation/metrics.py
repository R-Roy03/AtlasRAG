import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

class AtlasEvaluator:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        # Judge ke liye fast model use kar rahe hain
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=api_key,
            temperature=0
        )
        self.parser = JsonOutputParser()

        self.eval_prompt = PromptTemplate(
            input_variables=["question", "context", "answer"],
            template="""
            You are an AI Quality Assurance Judge. Evaluate the following RAG response.
            
            Question: {question}
            Retrieved Context: {context}
            Generated Answer: {answer}
            
            Provide a JSON output with two scores (0.0 to 1.0):
            1. "faithfulness": Does the answer come ONLY from the context? (1.0 = Yes, 0.0 = Hallucination)
            2. "relevance": Does the answer actually answer the question? (1.0 = Perfect, 0.0 = Irrelevant)
            
            Output strictly in JSON format: {{ "faithfulness": score, "relevance": score }}
            """
        )
        self.chain = self.eval_prompt | self.llm | self.parser

    def evaluate(self, question, context_docs, answer):
        # Context thoda trim karte hain taaki fast ho
        context_text = "\n".join([doc.page_content[:500] for doc in context_docs])
        try:
            print("⚖️  Atlas Judge is evaluating...")
            scores = self.chain.invoke({
                "question": question,
                "context": context_text,
                "answer": answer
            })
            return scores
        except Exception as e:
            print(f"❌ Eval Error: {e}")
            return {"faithfulness": 0.0, "relevance": 0.0}