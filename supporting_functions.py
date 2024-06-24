import json
from bs4 import BeautifulSoup
from notion_functions import NotionPage
from handler import Summarizer
from epub_functions import Book
import os
from dotenv import load_dotenv

def print_json(json_data):
    print(json.dumps(json_data, indent=4))

def save_json(json_data, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps(json_data, indent=4))

def load_json(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())

def create_book_content_html_and_serve_with_flask(book_content, file_details, folder_name):
    import os
    from flask import Flask, send_from_directory

    # Ensure the directory exists
    folder_path = os.path.join(folder_name, 'book_content')
    os.makedirs(folder_path, exist_ok=True)

    soup = BeautifulSoup('', 'html.parser')
    html_content = soup.new_tag('html')
    soup.append(html_content)
    head_tag = soup.new_tag('head') 
    html_content.append(head_tag)
    title_tag = soup.new_tag('title')
    title_tag.append("Book Content")
    head_tag.append(title_tag) 

    body_tag = soup.new_tag('body')
    html_content.append(body_tag)

    for file in file_details:
        header = soup.new_tag('h1')
        header.append(file['file_name'])
        body_tag.append(header)
        content_file = book_content.get_item_with_href(file['file_name'])
        content = content_file.get_body_content()
        if content:
            parsed_content = BeautifulSoup(content.decode('utf-8'), 'html.parser')  # Parse the content
            body_tag.append(parsed_content)  # Append parsed content to body
    
    # Save the html content to a file
    with open(os.path.join(folder_path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(str(html_content))

    # Serve the html content with Flask
    app = Flask(__name__)

    @app.route('/')
    def index():
        return send_from_directory(folder_path, 'index.html')
    
    app.run(port=5500)

def get_parsed_html_content(book_content, href):
    content_file = book_content.get_item_with_href(href)
    content = content_file.get_body_content()
    if content:
        soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')
        return soup.get_text()  # Extract text without HTML elements
    return None

   