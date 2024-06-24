import os
from dotenv import load_dotenv
from handler import Application

notion_parent_page_id = os.getenv('NOTION_PARENT_PAGE_ID')
book_path = './books/accelerating-ind/book.epub'
html_path = './books/four-thousand-weeks/highlights.html'
book_title = "Four Thousand Weeks: Time Management for Mortals"
chapters_to_skip = ["cover", "epigraph", "acknowledgements", "acknowledgment", "foreword", "dedication", "contents", "introduction", "prologue", "appendix", "bibliography", "index", "glossary", "about the author", "about the book", "about the publisher", "colophon", "title page", "blank page", "half title", "blank", "notes", "copyright"]
summary_instructions = "Focus on the ideas by different thinkers and phiolosophies. Also, focus on the techniques as well as strategies shared for time management."

if __name__ == '__main__':
    app = Application(book_path, html_path, summary_instructions, notion_parent_page_id, book_title, chapters_to_skip)
    app.start()
