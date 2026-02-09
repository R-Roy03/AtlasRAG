import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class LLMGenerator:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ Error: Google API Key missing")
            self.llm = None
            return

        # UPDATE: Using 'gemini-2.5-flash' from our available list
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.3
        )
        
        self.prompt = ChatPromptTemplate.from_template("""
        You are an expert AI Assistant named 'Atlas'.
        Use the following pieces of retrieved context to answer the question.
        If the answer is not in the context, just say that you don't know. 
        Keep the answer concise and professional.

        Context:
        {context}

        Question: 
        {question}

        Answer:
        """)
        
        self.chain = self.prompt | self.llm | StrOutputParser()

    def generate(self, query, context):
        if not self.llm:
            return "Error: LLM not initialized. Check API Key."
            
        try:
            response = self.chain.invoke({"context": context, "question": query})
            return response
        except Exception as e:
            return f"❌ Error generating response: {e}"