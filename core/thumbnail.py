import os
import pymupdf

THUMBNAIL_PATH = os.path.join("storage", "thumbnails")

class ThumbnailGenerator:
    def generate_thumbnail(self, pdf_path):
        document = pymupdf.open(pdf_path)
        page = document.load_page(0)
        pixels = page.get_pixmap()  # Low resolution via pixel compression

        base_name = os.path.basename(pdf_path).replace(".pdf", ".png")
        thumbnail_path = os.path.join(THUMBNAIL_PATH, base_name)

        pixels.save(thumbnail_path)

        document.close()

        return thumbnail_path
    
    def get_total_pages(self, pdf_path):
        document = pymupdf.open(pdf_path)
        total = len(document)
        document.close()

        return total
    
    


