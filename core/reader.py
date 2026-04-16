import pymupdf
import os


class PDFReader:
    def convert_pdf_to_images(self, pdf_path):
        folder_name = os.path.basename(pdf_path).replace(".pdf", "")
        output_dir = os.path.join("storage", "pdfs", folder_name)
        os.makedirs(output_dir, exist_ok=True)

        image_paths = []

        with pymupdf.open(pdf_path) as document:
            for i, page in enumerate (document):
                pix = page.get_pixmap(matrix=pymupdf.Matrix(2,2))
                img_path = os.path.join(output_dir, f"page_{i}.png")
                pix.save(img_path)
                image_paths.append(img_path)

        return image_paths