from crewai.tools import BaseTool
from PyPDF2 import PdfReader
from typing import List
from pydantic import BaseModel, Field

class TextSections(BaseModel):
    sections: List[str] = Field(..., description="List of strings that separate the original text in sections")

class PDFReaderTool(BaseTool):
    name: str = "PDF Reader Tool"
    description: str = "Reads and returns the raw text from a PDF file."

    def separateTextSections(self, text: str) -> TextSections:
        len_text = len(text)
        text_sections = TextSections(sections=[])
        # Uma seção apenas, logo o texto inteiro
        if(len_text < 1000):
            text_sections.sections = [text]
            return text_sections
        # Garantido ser mais do que uma seção
        else:
            sections = []
            amount_sections = 1
            if(len_text % 1000) != 0:
                amount_sections = (int(len_text // 1000)) + 1
            else:
                amount_sections = int(len_text // 1000)
            starting_character = 0
            current_character_index = 1000
            for sectionIndex in range(1, amount_sections + 1, 1):
                if(sectionIndex == amount_sections):
                    sections.append(text[starting_character:])
                    return sections
                else:
                    current_character = text[current_character_index]
                    while(current_character != "."):
                        current_character_index += 1
                        current_character = text[current_character_index]
                    current_character_index += 1
                    sections.append(text[starting_character:current_character_index])
                    starting_character = current_character_index 
                    current_character_index = (sectionIndex + 1) * 1000
            text_sections.sections = sections
            return text_sections      

    def _run(self, pdf_path: str) -> TextSections:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return str(self.separateTextSections(text))