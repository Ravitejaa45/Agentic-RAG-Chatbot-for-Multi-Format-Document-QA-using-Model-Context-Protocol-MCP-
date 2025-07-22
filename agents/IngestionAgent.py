from core.parser import parse_file
from core.mcp import create_mcp_message

class IngestionAgent:
    def process(self, uploaded_files):
        extracted_texts = [parse_file(file) for file in uploaded_files]
        return create_mcp_message(
            sender="IngestionAgent",
            receiver="RetrievalAgent",
            msg_type="CONTEXT_REQUEST",
            payload={"docs": extracted_texts}
        )