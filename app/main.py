import streamlit as st
import os
import sys
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from db.database import init_db
from core.services import DocumentService
from core.analytics import AnalyticsService
from util.emoji_ref import (
    ICON_DIVIDERS, 
    ICON_BOOK, 
    ICON_ARROW_LEFT, 
    ICON_ARROW_RIGHT, 
    ICON_SETTINGS2, 
    ICON_BROOM,
    ICON_WARNING,
    ICON_CHECK,
    ICON_CROSS
    )

# Manage session state
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "reader_mode" not in st.session_state:
    st.session_state.reader_mode = False

if "current_page" not in st.session_state:
    st.session_state.current_page = 0

if "upload_key" not in st.session_state:
    st.session_state.upload_key = 0

if "search_run" not in st.session_state:
    st.session_state.search_run = False

if "show_reset" not in st.session_state:
    st.session_state.show_reset = False

# Init
init_db()
load_dotenv(os.path.join(BASE_DIR, ".env"), override=True)

doc_service = DocumentService()
analytics_service = AnalyticsService()

database_file = os.path.join("data", "documents.db")
pdf_dir = os.path.join("storage", "pdfs")
thumbnail_dir = os.path.join("storage", "thumbnails")

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Page config
st.set_page_config(page_title="DocumentManager", layout="wide")
st.title(f"{ICON_DIVIDERS} Intelligent Document Manager")
st.divider()

st.subheader(f"{ICON_SETTINGS2} Admin Controls")
if st.button(f"{ICON_BROOM} Clean and Reset Database"):
    st.session_state.show_reset = True

if st.session_state.show_reset:
    st.text_input("Enter the Admin Password", type="password", key="admin_password")

    if st.button(f"{ICON_WARNING} Confirm Reset"):
        if st.session_state.admin_password == ADMIN_PASSWORD:

            import shutil

            # Delete DB
            if os.path.exists(database_file):
                os.remove(database_file)

            # Delete PDFs, Images, Thumbnails
            shutil.rmtree(pdf_dir, ignore_errors=True)
            shutil.rmtree(thumbnail_dir, ignore_errors=True)

            # Recreate empty directories
            os.makedirs(pdf_dir, exist_ok=True)
            os.makedirs(thumbnail_dir, exist_ok=True)

            st.success(f"{ICON_CHECK} System reset successfully.  App should be restarted.")
            st.session_state.show_reset = False
            st.rerun()
        else:
            st.error(f"{ICON_CROSS} The password entered is incorrect")

tabs = st.tabs(["Upload", "Search & View", "Analytics"])

# Tab 0: Upload document
with tabs[0]:
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], key=f"uploader_{st.session_state.upload_key}")
    tags = st.text_input("Tags (comma separated)", key=f"tags_{st.session_state.upload_key}")
    description = st.text_area("Description", key=f"desc_{st.session_state.upload_key}")
    lecture_date = st.date_input("Lecture Date (optional)", value=None, key=f"date_{st.session_state.upload_key}")

    if st.button("Upload"):
        analytics_service.record_app_visit("upload_click")
        if uploaded_file: 
            doc_service.upload_document(uploaded_file, tags, description, lecture_date)
            st.success(f"'{uploaded_file.name}' uploaded successfully.")
            st.session_state.upload_key += 1
            st.rerun()
        else:
            st.error("Please upload a file")

# Tab 1: Search and View
with tabs[1]:
    st.header("Search & View")

    col1, col2 = st.columns(2)
    with col1:
        search_tag = st.text_input("Search by Tag")
    with col2:
        search_date = st.date_input("Search by Date", value=None)

    if st.button("Search"):
        analytics_service.record_app_visit("search_click")
        st.session_state.search_results = doc_service.search_documents(
            tag=search_tag if search_tag else None,
            lecture_date=str(search_date) if search_date else None
        )
        st.session_state.search_run = True
        st.session_state.reader_mode = False
        st.session_state.selected_doc = None

    results = st.session_state.search_results

    if not st.session_state.reader_mode:
        if results:
            st.subheader(f"Results: {len(results)} documents")
            container = st.container(height=500)

            with container:
                for doc in results:
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        if doc.thumbnail_path:
                            st.image(doc.thumbnail_path, width=120)

                    with col2:
                        st.write(f"**{doc.name}**")
                        st.write(f"Tags: {doc.tags}")
                        st.write(f"Lecture Date: {doc.lecture_date}")

                        if st.button(f"Open", key=f"open_{doc.id}"):
                            analytics_service.record_app_visit("open_document")
                            st.session_state.selected_doc = doc
                            st.session_state.current_page = 0
                            st.session_state.reader_mode = True
                            st.rerun()
        else:
            if st.session_state.search_run:
                st.info("No results found. Try a different tag or date.")
             

    if st.session_state.reader_mode and st.session_state.selected_doc:
        doc = st.session_state.selected_doc

        col_back, col_title = st.columns([1, 8])
        with col_back:
            if st.button("<- Back to Results"):
                st.session_state.reader_mode = False
                st.rerun()

        st.subheader(f"{ICON_BOOK} Reading: {doc.name}")

        folder_name = os.path.basename(doc.path).replace(".pdf", "")
        image_dir = os.path.join("storage", "pdfs", folder_name)

        if not os.path.exists(image_dir):
            st.error("Images not found. PDF converstion may have failed")
        else:
            images = sorted(
                os.listdir(image_dir),
                key=lambda x: int(x.replace("page_", "").replace(".png", ""))
            )
            total_pages = doc.total_pages
            current_page = st.session_state.current_page

            st.write(f"Page {current_page + 1} of {total_pages}")

            col1, col2, col3 = st.columns([1, 6, 1])

            with col1:
                if st.button(f"{ICON_ARROW_LEFT} Previous"):
                    analytics_service.record_app_visit("previous_page")
                    if current_page > 0:
                        st.session_state.current_page -= 1
                        st.rerun()

            with col3:
                if st.button(f"Next {ICON_ARROW_RIGHT}"):
                    analytics_service.record_app_visit("next_page")
                    if current_page < total_pages - 1:
                        st.session_state.current_page += 1
                        st.rerun()

            img_path = os.path.join(image_dir, images[st.session_state.current_page])
            col1, col2, col3 = st.columns([1, 8, 1])
            with col2:
                st.image(img_path, width='stretch')

            # Record page visit analytics
            analytics_service.record_page_visit(doc.id, st.session_state.current_page)

            unique_pages = analytics_service.get_unique_pages_viewed(doc.id)
            progress = (unique_pages / doc.total_pages) * 100 if doc.total_pages else 0

            st.progress(progress / 100)
            st.write(f"Progress: {progress:.2f}% ({unique_pages}/{doc.total_pages})")

        # Progress
        if st.button("Close Reader"):
            analytics_service.record_app_visit("close_reader")
            st.session_state.reader_mode = False
            st.rerun()
    
# Tab 2: Analytics
with tabs[2]:
    st.subheader("Analytics")

    if st.button("Reset Analytics"):
        analytics_service.reset_analytics()
        st.success("Analytics data successfully reset")

    st.subheader("App Usage")

    app_data = analytics_service.get_app_visits()

    import pandas as pd

    df = pd.DataFrame(app_data, columns=["Event", "Count"])

    if df.empty:
        st.info("No analytics available to display.  Perform some actions to see insights.")
    else:
        st.bar_chart(df.set_index("Event"))

    st.subheader("Document Progress")

    all_documents = doc_service.get_all_documents()

    all_data = []

    for doc in all_documents:
        unique_pages = analytics_service.get_unique_pages_viewed(doc.id)
        progress =  (unique_pages / doc.total_pages) * 100 if doc.total_pages else 0

        all_data.append({
            "Document": doc.name,
            "Pages Read": unique_pages,
            "Total Pages": doc.total_pages,
            "Progress (%)": round(progress, 2)
        })

    df_docs = pd.DataFrame(all_data)
    st.dataframe(df_docs)
