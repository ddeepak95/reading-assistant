import os
from dotenv import load_dotenv
from handler import Application

notion_parent_page_id = os.getenv('NOTION_PARENT_PAGE_ID')
book_path = './books/buddhism/book.epub'
html_path = './books/buddhism/highlights.html'
book_title = "Why Buddhism is True"
chapters_to_skip = ["cover", "epigraph", "acknowledgements", "acknowledgment", "foreword", "dedication", "contents", "introduction", "prologue", "appendix", "bibliography", "index", "glossary", "about the author", "about the book", "about the publisher", "colophon", "title page", "blank page", "half title", "blank", "notes", "copyright"]
summary_instructions = "Focus on the buddhism concepts and the scientific ideas shared."

if __name__ == '__main__':
    app = Application(book_path, html_path, summary_instructions, notion_parent_page_id, book_title, chapters_to_skip)
    app.start()
