# Warning control
import warnings
warnings.filterwarnings('ignore')

import os
import sys
from resumidor_pdfs.crew import ResumidorPdfs

def load_multiple_pdfs(folder_path):
    inputs = []
    folder_path = os.path.abspath(folder_path)  

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"): 
            file_path = os.path.abspath(os.path.join(folder_path, filename))  
            inputs.append({"pdf_path": file_path, "name_of_pdf": filename[:-4]})
    
    return inputs

def run():
    inputs = load_multiple_pdfs('..\\pdfs')

    try:
        ResumidorPdfs().crew().kickoff_for_each(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    inputs = load_multiple_pdfs('..\\pdfs')

    try:
        ResumidorPdfs().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs[0])

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    try:
        ResumidorPdfs().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    inputs = load_multiple_pdfs('..\\pdfs')
    
    try:
        ResumidorPdfs().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs[0])

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
