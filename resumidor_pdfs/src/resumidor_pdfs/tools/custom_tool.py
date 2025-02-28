from crewai.tools import BaseTool
from PyPDF2 import PdfReader

class PDFReaderTool(BaseTool):
    name: str = "Leitor de PDF"
    description: str = "Lê o conteúdo de um arquivo PDF e retorna o texto."

    def _run(self, pdf_path: str) -> str:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text