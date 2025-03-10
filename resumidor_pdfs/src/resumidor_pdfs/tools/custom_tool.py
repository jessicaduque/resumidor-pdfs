from crewai.tools import BaseTool
from PyPDF2 import PdfReader
from typing import List, Type
from pydantic import BaseModel, Field

class PDFText(BaseModel):
    text_string: str = Field(..., description="Raw text extracted from a PDF file")

    def __init__(self):
        super().__init__()

    def get_field_info_json(self) -> str:
        field_info = "\n"
        for field_name, field_instance in self.model_fields.items():
            field_info += field_name + ", described as: " + field_instance.description + "\n"
        return field_info


class PDFReaderTool(BaseTool):
    name: str = "PDF Reader Tool"
    description: str = "Reads and returns a PDFText with the text from a PDF file"

    def _run(self, pdf_path: str) -> PDFText:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        pdf_text = PDFText(text_string=text)
        return pdf_text
    
class TextSections(BaseModel):
    sections: List[str] = Field(..., description="List of strings that separate the original text in sections")

class SeparateTextSectionsTool(BaseTool):
    name: str = "Text Section Separator Tool"
    description: str = "With a PDFText, separates it into different sections to create a TextSections structure"

    def _run(self, text_string: str) -> TextSections:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        text = text_string
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
                amount_sections = int(len_text % 1000) + 1
            else:
                amount_sections = int(len_text % 1000)
            starting_character = 0
            current_character_index = 1000
            for sectionIndex in range(1, amount_sections + 1, 1):
                print("STARTING CHARACTER: " + starting_character)
                print("CURRENT CHARACTER: " + current_character_index)
                if(sectionIndex == amount_sections):
                    sections.append(text[starting_character:])
                    return sections
                else:
                    current_character = text[current_character_index]
                    while(current_character != "."):
                        current_character_index += 1
                        current_character = text[current_character_index]
                    current_character += 1
                    sections.append(text[starting_character:current_character])
                    starting_character = current_character_index 
                    current_character_index = (sectionIndex + 1) * 1000
            text_sections.sections = sections
            return text_sections