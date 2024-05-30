import streamlit as st
import pandas as pd
from pypdf import PdfReader, PdfWriter
from pdf_functions import get_chapters_from_pdf, get_text_for_selected_chapters_pdf
from epub_functions import get_chapters_from_epub
import copy


# Initialize the flag in session state
if "new_file_uploaded" not in st.session_state:
    st.session_state.new_file_uploaded = False

if "file_processed" not in st.session_state:
    st.session_state.file_processed = False

if "chapters" not in st.session_state:
    st.session_state.chapters = []

if "reader" not in st.session_state:
    st.session_state.reader = None

if "selected_chapters" not in st.session_state:
    st.session_state.selected_chapters = []

if "uploaded_file_format" not in st.session_state:
    st.session_state.uploaded_file_format = ""

if "selected_chapters_text" not in st.session_state:
    st.session_state.selected_chapters_text = []



# Title
st.title('Summarize book as a Notion page')
st.header ('Upload the book')

# Upload pdf or epub or mobi file
uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'epub', 'mobi'])



# Container to list chapters
chapters_container = st.container(height=300, border=True)

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

def get_chapter_text():
    if st.session_state.button_clicked:
        if not st.session_state.selected_chapters:
            st.warning('No chapters selected. Please select at least one chapter.')
        else:
            # Perform the action for the button here
            if st.session_state.uploaded_file_format == 'application/pdf':
                st.session_state.selected_chapters_text = get_text_for_selected_chapters_pdf(st.session_state.selected_chapters, st.session_state.reader)
            elif st.session_state.uploaded_file_format == 'application/epub+zip':
                st.session_state.selected_chapters_text = copy.deepcopy(st.session_state.selected_chapters)
        st.session_state.button_clicked = False

if st.button('Get the chapter text'):
    st.session_state.button_clicked = True
    get_chapter_text()





# Container to show the text of the selected chapters
text_container = st.container(height=500, border=True)


def get_chapters_and_write_title_in_container(chapters):
    with chapters_container:
        # Create a list of all chapters with an additional 'selected' field
        all_chapters = [{**chapter, 'selected': st.checkbox(chapter['title'], value=False)} for chapter in chapters]
        # Filter the list to only include selected chapters
        st.session_state.selected_chapters = [chapter for chapter in all_chapters if chapter['selected']]


if uploaded_file is not None:
    st.session_state.new_file_uploaded = True

# update the uploaded file format after the file is uploaded
if st.session_state.new_file_uploaded:
    # Reset session state variables

    st.session_state.uploaded_file_format = uploaded_file.type
    if st.session_state.uploaded_file_format == 'application/pdf':
        st.session_state.chapters = get_chapters_from_pdf(uploaded_file).get('chapters')
        st.session_state.reader = get_chapters_from_pdf(uploaded_file).get('reader')
    if st.session_state.uploaded_file_format == 'application/epub+zip':
        st.session_state.chapters = get_chapters_from_epub(uploaded_file).get('chapters')

    # Set the flag to True after processing the file
    st.session_state.file_processed = True
    # Set new_file_uploaded to False after processing the file
    st.session_state.new_file_uploaded = False

# Call the function to render checkboxes outside of the if statement
if st.session_state.chapters:
    get_chapters_and_write_title_in_container(st.session_state.chapters)

# Write the text of the selected chapters to the text container
if st.session_state.selected_chapters_text:
    with text_container:
        for chapter in st.session_state.selected_chapters_text:
            st.header(chapter['title'])
            st.write(chapter['content'])

        




        









            
        

    
