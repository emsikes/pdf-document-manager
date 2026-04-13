# Upload document
from db.repository import DocumentRepository
from core.file_manager import FileManager
from core.thumbnail import ThumbnailGenerator


class DocumentService:
    def __init__(self):
        self.repo = DocumentRepository()
        self.file_manager = FileManager()
        self.thumbnail_generator = ThumbnailGenerator()

    def upload_document(self, uploaded_file, tags, description, lecture_date=None):
        """
        1. Save fie (with timestamp)
        2. Generate thumbnail
        3. Get total # of pages
        4. Convert to images
        5. Create required variables
        6. Save to database
        """

        document = []
        file_path = self.file_manager.save_file(uploaded_file)
        thumbnail_path = self.thumbnail_generator.generate_thumbnail(file_path)
        total_pages = self.thumbnail_generator.get_total_pages(file_path)
       
        # self.repo.add_document(document)