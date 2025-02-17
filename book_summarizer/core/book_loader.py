from typing import Optional, List, Dict
import os
from tinydb import TinyDB, Query
from ebooklib import epub
from ..utils.file_operations import copy_and_rename_file
from ..models.schemas import Book

class DocumentHandler:
    def __init__(self, main_db: TinyDB, highlights_db: TinyDB):
        self.main_db = main_db
        self.highlights_db = highlights_db
        self.Item = Query()

    def create_doc_id(self, doc_name: str) -> str:
        base_id = doc_name.lower().replace(" ", "-")
        doc_id = base_id
        counter = 1

        while self.main_db.contains(self.Item.uid == doc_id):
            doc_id = f"{base_id}-{counter}"
            counter += 1

        return doc_id

    def load_document(self, 
                     doc_name: str, 
                     doc_source: str, 
                     highlights_source: Optional[str] = None,
                     working_base_dir: str = "./data/srcs/") -> str:
        """
        Load a new document into the system.
        
        Args:
            doc_name: Name of the document
            doc_source: Path to the epub file
            highlights_source: Optional path to the highlights file
            working_base_dir: Base directory for working files
        
        Returns:
            str: The doc_id of the loaded document
        """
        # Create document ID and working directory
        doc_id = self.create_doc_id(doc_name)
        working_folder = os.path.join(working_base_dir, doc_id)
        
        # Create uploads directory
        uploads_dir = os.path.join(working_folder, "uploads")
        os.makedirs(uploads_dir, exist_ok=True)

        # Copy and save the document file
        doc_dest = copy_and_rename_file(doc_source, uploads_dir, "source_doc")
        if not doc_dest:
            raise Exception("Failed to copy document file")

        # Insert basic document info into main DB
        self.main_db.insert({
            "uid": doc_id,
            "name": doc_name,
            "folder": working_folder
        })

        # Process highlights if provided
        if highlights_source:
            highlights_dest = copy_and_rename_file(
                highlights_source, 
                uploads_dir, 
                "highlights_doc"
            )
            if highlights_dest:
                self._process_highlights(highlights_dest, doc_id)

        # Process epub file
        self._process_epub(doc_dest, working_folder, doc_id)
        
        return doc_id

    def list_documents(self) -> List[Book]:
        """
        Get a list of all documents in the system.
        
        Returns:
            List of Book objects containing document details
        """
        docs = self.main_db.all()
        return [Book(**doc) for doc in docs]

    def get_document(self, doc_id: str) -> Optional[Book]:
        """
        Get details of a specific document.
        
        Args:
            doc_id: ID of the document to retrieve
            
        Returns:
            Book object if found, None otherwise
        """
        doc = self.main_db.get(self.Item.uid == doc_id)
        return Book(**doc) if doc else None

    def get_document_highlights(self, doc_id: str) -> List[Dict]:
        """
        Get all highlights for a specific document.
        
        Args:
            doc_id: ID of the document
            
        Returns:
            List of highlights for the document
        """
        doc_highlights = self.highlights_db.get(self.Item.uid == doc_id)
        return doc_highlights.get('kindle_highlights', []) if doc_highlights else []

    def _process_epub(self, epub_path: str, working_folder: str, doc_id: str):
        """Process the epub file and extract its contents"""
        book = epub.read_epub(epub_path)
        
        # Extract TOC
        toc = self._get_toc_details(book)
        self.main_db.update(
            {'toc': toc}, 
            self.Item.uid == doc_id
        )

        # Extract contents
        output_dir = os.path.join(working_folder, "unbundled_epub")
        file_details = []
        
        for item in book.get_items():
            file_path = os.path.join(output_dir, item.file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'wb') as f:
                f.write(item.content)
                
            file_details.append({
                'file_name': os.path.basename(item.file_name),
                'file_ext': os.path.splitext(item.file_name)[1][1:],
                'file_path': item.file_name
            })

        self.main_db.update(
            {'children_file_details': file_details}, 
            self.Item.uid == doc_id
        )

    def _get_toc_details(self, book: epub.EpubBook) -> list:
        """Extract table of contents details from epub book"""
        toc = book.toc
        toc_details = []
        
        for item in toc:
            if isinstance(item, epub.Link):
                toc_item = {
                    "type": "link",
                    "href": item.href,
                    "title": item.title,
                    "uid": item.uid
                }
            elif isinstance(item, tuple) and isinstance(item[0], epub.Section):
                toc_item = {
                    "type": "section",
                    "title": item[0].title,
                    "links": []
                }
                for link in item[1]:
                    toc_item["links"].append({
                        "type": "link",
                        "href": link.href,
                        "title": link.title,
                        "uid": link.uid
                    })
            toc_details.append(toc_item)
            
        return toc_details

    def _process_highlights(self, highlights_path: str, doc_id: str):
        """Process highlights file and store in highlights database"""
        from .highlight_processor import HighlightProcessor
        
        # Create highlight processor
        highlight_processor = HighlightProcessor(self.highlights_db)
        
        # Process and store highlights
        highlight_processor.process_highlights(
            highlights_path=highlights_path,
            doc_id=doc_id
        ) 