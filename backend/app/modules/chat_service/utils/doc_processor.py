import logging 
import io
import asyncio
import polars as pl
from typing import List
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitter import RecursiveCharacterTextSplitter


logger = logging.Logger(__name__)

class DocProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=200,
            add_start_index=True,
        )

        self.DOCS_TYPES  = {
            "pdf": self._process_pdf,
            "csv": self._process_csv,
            "excel": self._process_excel,
            "xlsx": self._process_excel,
            "xls": self._process_excel,
            "mdx": self._process_text,
            "md": self._process_text,
            "text": self._process_text,
            "txt": self._process_text,
        }

    async def process(self, doc_content: bytes, file_type: str) -> List[Document]:
        file_type = file_type.lower().split(".").replace("application/", "")
        handler = self.DOCS_TYPES.get(file_type)
        if not handler:
            logger.warning(f"Unsupported file type: {file_type}")
            handler = self._process_text
            
            try:
                logger.info(f"Processing {file_type} document")
                documents = await asyncio.to_thread(handler, doc_content)
                logger.info(f"Successfully processed {file_type} document")
                return documents
            except Exception as e:
                logger.error(f"Failed to process {file_type} document: {e}")
                return[]

    def _process_pdf(self, content: bytes) -> List[Document]:
        """Extract text from PDF document"""
        text = ""
        try:
            reader = PdfReader(io.BytesIO(content))
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            logger.error(f"Failed to extract text from PDF document: {e}")
            return[]

        return self.text_splitter.create_documents([text])
    
    def _process_csv(self, content: bytes) -> List[Document]:
        """Extract text from CSV document using polars"""
        try:
            df = pl.read_csv(io.BytesIO(content))
            text_data = []
            for row in df.iter_rows(named=True):
                row_str = "\n".join(f"{k}: {v}" for k, v in row.items() if v is not None)
                text_data.append(row_str)
            return self.text_splitter.create_documents(text_data)

        except Exception as e:
            logger.error(f"Failed to extract text from CSV document: {e}")
            return[]


    def _process_excel(self, content: bytes) -> List[Document]:
        """Extract text from Excel document using polars"""
        try:
            df = pl.read_excel(io.BytesIO(content))
            text_data = []
            for row in df.iter_rows(named=True):
                row_str = "\n".join(f"{k}: {v}" for k, v in row.items() if v is not None)
                text_data.append(row_str)
            return self.text_splitter.create_documents(text_data)

        except Exception as e:
            logger.error(f"Failed to extract text from Excel document: {e}")
            return[]     

    def _process_text(self, content: bytes) -> List[Document]:
        """Extract text from text document"""
        try:
            text = content.decode("utf-8", errors="ignore")
            return self.text_splitter.create_documents([text])
        except Exception as e:
            logger.error(f"Failed to extract text from text document: {e}")
            return[]