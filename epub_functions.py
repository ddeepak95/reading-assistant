import tempfile
import shutil
import ebooklib
from ebooklib import epub
import streamlit as st
from bs4 import BeautifulSoup

def get_chapters_from_epub(epub_file_obj):
    with tempfile.NamedTemporaryFile(delete=False) as temp_epub_file:
        shutil.copyfileobj(epub_file_obj, temp_epub_file)
        temp_epub_file_path = temp_epub_file.name

    book = epub.read_epub(temp_epub_file_path)
    chapters = []
    for index, a in enumerate(book.toc):
        if isinstance(a, ebooklib.epub.Link):
            chapter = {}
            chapter['id'] = a.uid if a.uid else f'chapter_{index}'
            chapter['title'] = a.title
            chapter['href'] = a.href
            chapters.append(chapter)
        elif isinstance(a, tuple):
            # Handle the case where 'a' is a tuple
            section, links = a
            for link in links:
                chapter = {}
                chapter['id'] = link.uid if link.uid else f'chapter_{index}'
                chapter['title'] = link.title
                chapter['href'] = link.href
                chapters.append(chapter)

    # for chapter in chapters:
    #     href_base, _, href_locator = chapter['href'].partition('#')
    #     item = book.get_item_with_href(href_base)
    #     if item:
    #         soup = BeautifulSoup(item.get_body_content(), 'html.parser')
    #         if href_locator:
    #             element = soup.find(id=href_locator)
    #             chapter['content'] = element.get_text() if element else ''
    #         else:
    #             chapter['content'] = soup.get_text()
    st.write(chapters)
    href="OEBPS/part0008.xhtml"
    href_base, _, href_locator = href.partition('#')
    item = book.get_item_with_href(href_base)
    st.write(item.get_body_content())
    if item:
        soup = BeautifulSoup(item.get_body_content(), 'html.parser')
        if href_locator:
            element = soup.find(id=href_locator)
            chapter['content'] = element.get_text() if element else ''
        else:
            chapter['content'] = soup.get_text()





    return {'chapters': chapters}