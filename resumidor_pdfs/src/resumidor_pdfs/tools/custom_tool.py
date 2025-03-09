from crewai.tools import BaseTool
from PyPDF2 import PdfReader
from typing import List
from pydantic import BaseModel, Field


class PDFReaderTool(BaseTool):
    name: str = "PDF Reader Tool"
    description: str = "Reads and returns the raw text from a PDF file."

    def _run(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    
class TextSections(BaseModel):
    argument: List[str] = Field(..., description="List of strings that separate the original text in sections")