from groq import Groq
from core.mcp import create_mcp_message
import os
from dotenv import load_dotenv

load_dotenv()

class LLMResponseAgent:
    def __init__(self, retriever):
        self.retriever = retriever
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def process(self, message):
        query = message["payload"]["query"]
        top_chunks = self.retriever.retrieve_top_chunks(query)
        context = "\n\n".join(top_chunks)
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

        response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content.strip()
        return create_mcp_message(
            sender="LLMResponseAgent",
            receiver="User",
            msg_type="RESPONSE",
            trace_id=message["trace_id"],
            payload={"answer": answer, "sources": top_chunks}
        )