import os
import time
import csv
import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class LLMGenerator:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = "gemini-flash-latest"
        
        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=api_key,
            temperature=0.3
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question", "chat_history"],
            template="""
            You are 'Atlas', an enterprise-grade AI assistant. 
            Use the retrieved context and chat history to answer the question.
            
            --- CHAT HISTORY ---
            {chat_history}
            --------------------

            --- RETRIEVED CONTEXT ---
            {context}
            -------------------------

            QUESTION: {question}
            
            ANSWER:
            """
        )
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def log_request(self, query, response, latency, context_count):
        # Logs folder ensure karo
        os.makedirs("logs", exist_ok=True)
        log_file = "logs/query_logs.csv"
        file_exists = os.path.isfile(log_file)
        
        with open(log_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Timestamp", "Query", "Response_Length", "Latency_Seconds", "Contexts_Retrieved", "Model"])
            
            writer.writerow([
                datetime.datetime.now().isoformat(),
                query,
                len(response),
                f"{latency:.2f}",
                context_count,
                self.model_name
            ])

    def generate_answer(self, query, retrieved_docs, history=[]):
        start_time = time.time()
        context_text = "\n\n".join([doc.page_content for doc in retrieved_docs])
        history_text = "\n".join([f"{msg['role'].title()}: {msg['content']}" for msg in history[-5:]])
        
        print(f"🤖 Atlas Generating answer...")
        
        try:
            response = self.chain.invoke({
                "context": context_text, 
                "question": query,
                "chat_history": history_text
            })
            
            end_time = time.time()
            self.log_request(query, response, end_time - start_time, len(retrieved_docs))
            return response
        except Exception as e:
            return f"⚠️ Error: {e}"