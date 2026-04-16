# 🗂️ Intelligent Document Manager

![Python](https://img.shields.io/badge/Python-3.12.3-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56.0-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.27.2-00A86B?style=flat&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)

A Streamlit-based PDF document management portal with upload, thumbnail generation, full-page image conversion, tagging, and SQLite persistence.

---

## Features

- **PDF Upload** — uploads stored with timestamps to prevent filename collisions
- **Thumbnail Generation** — first-page thumbnail auto-generated on upload
- **Page Extraction** — all PDF pages converted to high-resolution PNG images (2x matrix)
- **Metadata** — tags, description, lecture date, and upload date captured per document
- **SQLite Storage** — lightweight local database, zero configuration required
- **Search & View** *(coming soon)*
- **Analytics** *(coming soon)*

---

## Project Structure

```
document-manager/
├── app/
│   └── main.py               # Streamlit entry point
├── core/
│   ├── file_manager.py       # File saving with timestamp naming
│   ├── models.py             # Document dataclass
│   ├── reader.py             # PDF → PNG page extraction (PyMuPDF)
│   ├── services.py           # Upload orchestration
│   └── thumbnail.py          # First-page thumbnail generation
├── db/
│   ├── database.py           # SQLite init and connection
│   └── repository.py         # Document CRUD operations
├── storage/
│   ├── pdfs/                 # Raw uploaded PDFs (timestamped)
│   └── thumbnails/           # Generated thumbnail PNGs
├── data/
│   └── documents.db          # SQLite database
├── util/
│   └── emoji_ref.py          # Unicode emoji constants
├── tests/
│   └── path.ipynb
└── requirements.txt
```

---

## Tech Stack

| Library | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [PyMuPDF](https://pymupdf.readthedocs.io) | PDF parsing, thumbnail and image extraction |
| `sqlite3` | Local database (stdlib) |
| `datetime`, `os` | File management and timestamps (stdlib) |

---

## Getting Started

### 1. Clone the repo

```bash
git clone <repo-url>
cd document-manager
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create required storage directories

```bash
mkdir -p storage/pdfs storage/thumbnails data
```

### 5. Run the app

```bash
streamlit run app/main.py
```

---

## Storage Layout

Uploaded files are stored under `storage/` and never overwrite each other:

```
storage/
├── pdfs/
│   ├── 20260416093012_lecture1.pdf        # timestamped original
│   └── 20260416093012_lecture1/           # extracted page images
│       ├── page_0.png
│       ├── page_1.png
│       └── ...
└── thumbnails/
    └── 20260416093012_lecture1.png        # first-page thumbnail
```

---

## Database Schema

```sql
CREATE TABLE documents (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT,
    path           TEXT,
    thumbnail_path TEXT,
    tags           TEXT,
    description    TEXT,
    upload_date    TEXT,
    lecture_date   TEXT,
    total_pages    INTEGER
);
```

---

## Roadmap

- [ ] Search and filter by tags, date, description
- [ ] Document viewer (page-by-page image display)
- [ ] Analytics dashboard (upload trends, tag frequency)
- [ ] Bulk upload support
- [ ] Export / delete documents
