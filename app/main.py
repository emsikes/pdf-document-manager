import streamlit as st
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from db.database import init_db
from core.services import DocumentService
from util.emoji_ref import ICON_DIVIDERS


init_db()
doc_service = DocumentService()

st.set_page_config(page_title="DocumentManager", layout="wide")
st.title(f"{ICON_DIVIDERS} Intelligent Document Manager")
st.divider()

tabs = st.tabs(["Upload", "Search and View", "Analytics"])

with tabs[0]:
    # Upload
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    tags = st.text_input("Tags (comma separated)")
    description = st.text_area("Description")
    lecture_date = st.date_input("Lecture Date (optional)", value=None)

    if st.button("Upload"):
        if uploaded_file: 
            doc_service.upload_document(uploaded_file, tags, description, lecture_date)
        else:
            st.error("Please uplad a file")

with tabs[1]:
    # Search and view
    pass

with tabs[2]:
    # Analytics
    pass