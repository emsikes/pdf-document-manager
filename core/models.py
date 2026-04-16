from dataclasses import dataclass
from datetime import date


@dataclass
class Document:
    id: int | None
    name: str
    path: str
    thumbnail_path: str
    tags: str
    description: str
    upload_date: str
    lecture_date: date | None
    total_pages: int