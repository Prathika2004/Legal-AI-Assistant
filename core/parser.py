import fitz  # PyMuPDF
from docx import Document

class ContractParser:
    @staticmethod
    def extract_text(uploaded_file):
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            text = ""
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
            return text
            
        elif file_extension in ['docx', 'doc']:
            doc = Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs])
            
        else: # Plain text
            return str(uploaded_file.read(), "utf-8")