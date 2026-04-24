# Upload document
from datetime import datetime

from db.repository import DocumentRepository
from core.file_manager import FileManager
from core.thumbnail import ThumbnailGenerator
from core.reader import PDFReader
from core.models import Document



class DocumentService:
    def __init__(self):
        self.repo = DocumentRepository()
        self.file_manager = FileManager()
        self.thumbnail_generator = ThumbnailGenerator()
        self.pdf_reader = PDFReader()

    def upload_document(self, uploaded_file, tags, description, lecture_date=None):
        """
        1. Save file (with timestamp)
        2. Generate thumbnail
        3. Get total # of pages
        4. Convert to images
        5. Save to database
        """

        file_path = self.file_manager.save_file(uploaded_file)
        thumbnail_path = self.thumbnail_generator.generate_thumbnail(file_path)
        total_pages = self.thumbnail_generator.get_total_pages(file_path)
        self.pdf_reader.convert_pdf_to_images(file_path)

        document = Document(
            id=None,
            name=uploaded_file.name,
            path=file_path,
            thumbnail_path=thumbnail_path,
            tags=tags,
            description=description,
            upload_date=datetime.now().strftime("%Y-%m-%d"),
            lecture_date=lecture_date,
            total_pages=total_pages
        )
       
        self.repo.add_document(document)

    def search_documents(self, tag=None, lecture_date=None):
        return self.repo.search_documents(tag, lecture_date)
    
    def get_all_documents(self):
        return self.repo.get_all_documents()