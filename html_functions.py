from bs4 import BeautifulSoup
from copy import deepcopy
import os

class KindleHTMLParser:
    def __init__(self, html_file):
        self.html_file = html_file
        with open(self.html_file, 'r', encoding='utf-8') as f:
            self.soup = BeautifulSoup(f, 'html.parser')
        self.highlights = self.find_chapter_titles_and_highlights()

    def find_chapter_titles_and_highlights(self):
        body = self.soup.find('body')
        elements = body.find_all(attrs={"class": ["sectionHeading", "noteText"]})
        result = []
        for element in elements:
            chapter = {}
            if element.get('class') == ['sectionHeading']:
                chapter['title'] = element.text
                chapter['highlights'] = []
                result.append(chapter)
            elif element.get('class') == ['noteText']:
                new_element = deepcopy(element)
                for tag in new_element.find_all(['h2','h3']):
                    tag.decompose()
                text = new_element.get_text(strip=True)
                if len(result) > 0:
                    result[-1]['highlights'].append(text)
        return result
    
# Create a html file with the book content and highlights chapter wise

def create_html(directory, book_chapters, highlights):
    # Create a new BeautifulSoup object
    soup = BeautifulSoup('', 'html.parser')

    # Create the basic structure of the HTML document
    html_tag = soup.new_tag('html')
    soup.append(html_tag)

    head_tag = soup.new_tag('head')
    html_tag.append(head_tag)

    title_tag = soup.new_tag('title')
    title_tag.string = 'Preview: Chapter Content and Highlights'
    head_tag.append(title_tag)

    link_tag = soup.new_tag('link', rel='stylesheet', href='https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css')
    head_tag.append(link_tag)

    style_tag = soup.new_tag('style')
    style_tag.string = """
    .scrollable-content, .highlights-container { max-height: 500px; overflow-y: auto; }
    """
    head_tag.append(style_tag)

    body_tag = soup.new_tag('body')
    html_tag.append(body_tag)

    container_div = soup.new_tag('div', **{'class': 'container'})
    body_tag.append(container_div)

    # Add chapters and highlights to the HTML document
    for chapter in book_chapters:
        chapter_div = soup.new_tag('div', **{'class': 'my-5'})
        container_div.append(chapter_div)

        h1_tag = soup.new_tag('h1')
        h1_tag.string = chapter['title']
        chapter_div.append(h1_tag)

        highlights_div = soup.new_tag('div', **{'class': 'my-3'})
        chapter_div.append(highlights_div)
        chapter_div.append(soup.new_tag('hr'))
        h5_tag = soup.new_tag('h5')
        h5_tag.string = f'Highlights From Kindle '
        highlights_div.append(h5_tag)
        hightlights_list_div = soup.new_tag('div', **{'class': 'highlights-container'})
        highlights_div.append(hightlights_list_div)
        highlights_count = 0
        for highlight in highlights:
            if highlight['title'] == chapter['title']:
                highlights_count = len(highlight['highlights'])
                for h in highlight['highlights']:
                    alert_div = soup.new_tag('div', **{'class': 'alert alert-primary', 'role': 'alert'})
                    alert_div.string = h
                    hightlights_list_div.append(alert_div)
        highlights_count_tag = soup.new_tag('span', **{'class': 'badge badge-secondary'})
        highlights_count_tag.string = f'{highlights_count}'
        h5_tag.append(highlights_count_tag)

        content_div = soup.new_tag('div', **{'class': 'my-3'})
        chapter_div.append(content_div)

        h5_tag = soup.new_tag('h5')
        h5_tag.string = 'Chapter Content From EPUB'
        content_div.append(h5_tag)

        scrollable_div = soup.new_tag('div', **{'class': 'scrollable-content bg-light rounded p-3'})
        content_div.append(scrollable_div)

        p_tag = soup.new_tag('p')
        p_tag.string = chapter['content']
        scrollable_div.append(p_tag)

    # Write the HTML content to a file
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(directory + 'index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
