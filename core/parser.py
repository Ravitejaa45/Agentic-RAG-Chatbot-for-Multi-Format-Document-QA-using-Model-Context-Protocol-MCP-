import tempfile
from pathlib import Path
from docling.document_converter import DocumentConverter

converter = DocumentConverter()

def parse_file(uploaded_file):
    suffix = Path(uploaded_file.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = Path(tmp_file.name)

    result = converter.convert(source=str(tmp_path))
    doc = result.document
    return doc.export_to_markdown()
