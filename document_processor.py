import PyPDF2
import pandas as pd
from fastapi import UploadFile
import magic
import io

class DocumentProcessor:
    def __init__(self):
        self.supported_types = {
            'application/pdf': self._process_pdf,
            'text/csv': self._process_csv,
            'text/plain': self._process_text,
        }
    
    async def process_file(self, file: UploadFile) -> str:
        """
        Process an uploaded file and return its content as text.
        """
        content = await file.read()
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(content)
        
        if file_type not in self.supported_types:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        processor = self.supported_types[file_type]
        return await processor(content)
    
    async def _process_pdf(self, content: bytes) -> str:
        """
        Extract text from PDF content.
        """
        pdf_file = io.BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text
    
    async def _process_csv(self, content: bytes) -> str:
        """
        Process CSV content and convert to text format.
        """
        df = pd.read_csv(io.BytesIO(content))
        return df.to_string()
    
    async def _process_text(self, content: bytes) -> str:
        """
        Process plain text content.
        """
        return content.decode('utf-8') 