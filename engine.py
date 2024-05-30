import streamlit as st
from pypdf import PdfReader, PdfWriter
from pdf_functions import get_chapters_from_pdf, get_text_for_selected_chapters_pdf

# function to parse the uploaded file into chapters
def handler(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == 'application/pdf':
            # parse pdf
            chapters = get_chapters_from_pdf(uploaded_file)
            selected_chapters = []
            for chapter in chapters:
                selected_chapters.append(st.checkbox(chapter['title'], value=False))
            if st.button('Get text from selected chapters'):
                selected_chapters = [chapter for i, chapter in enumerate(chapters) if selected_chapters[i]]
                reader = PdfReader(uploaded_file)
                chapters_with_text = get_text_for_selected_chapters(selected_chapters, reader)
                st.write(chapters_with_text)

        elif uploaded_file.type == 'application/epub+zip':
            # parse epub
            pass
        elif uploaded_file.type == 'application/x-mobipocket-ebook':
            # parse mobi
            pass
        else:
            st.write('Unsupported file format. Please upload a pdf, epub or mobi file')
    else:
        st.write('Please upload a file')


