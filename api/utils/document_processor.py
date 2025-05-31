from pathlib import Path
from typing import List, Dict, Any
import logging
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import Document, NodeWithScore
# import magic # Removed
# from PIL import Image # Removed
# import io # Seems unused, removing

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1024, chunk_overlap: float = 0.25):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.node_parser = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=int(chunk_size * chunk_overlap)
        )
        self.pdf_reader = PDFReader()

    def process_file(self, file_path: Path) -> List[Document]:
        """Process a file and return a list of documents."""
        try:
            # mime = magic.Magic(mime=True) # Removed
            # file_type = mime.from_file(str(file_path)) # Removed
            file_extension = file_path.suffix.lower()

            if file_extension == '.pdf':
                return self._process_pdf(file_path)
            # You can add support for other file types here based on extension
            # elif file_extension == '.txt':
            #     return self._process_txt(file_path) # Example
            else:
                # Fallback or raise error for unsupported types
                logger.warning(f"Unsupported file extension: {file_extension}. Only .pdf is currently supported.")
                raise ValueError(f"Unsupported file extension: {file_extension}. Only .pdf is currently supported.")

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}", exc_info=True)
            raise

    def _process_pdf(self, file_path: Path) -> List[Document]:
        """Process PDF file with special handling for tables and images."""
        try:
            # Load PDF with enhanced metadata
            documents = self.pdf_reader.load_data(file_path)

            # Process each document
            processed_docs = []
            for doc in documents:
                # Extract metadata
                metadata = doc.metadata
                
                # Create enhanced document with metadata
                enhanced_doc = Document(
                    text=doc.text,
                    metadata={
                        **metadata,
                        'file_name': file_path.name,
                        'file_type': 'pdf',
                        'page_number': metadata.get('page_number', 0),
                        'has_tables': 'table' in doc.text.lower(),
                        'has_images': bool(metadata.get('images', []))
                    }
                )
                processed_docs.append(enhanced_doc)

            return processed_docs

        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}", exc_info=True)
            raise

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks with overlap."""
        try:
            nodes = self.node_parser.get_nodes_from_documents(documents)
            return [
                Document(
                    text=node.get_content(),
                    metadata=getattr(node, 'metadata', {})
                )
                for node in nodes
            ]
        except Exception as e:
            logger.error(f"Error splitting documents: {str(e)}", exc_info=True)
            raise 