import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from multiprocessing import Pool

class Book:
    def __init__(self, book_source, chapters_to_skip):
        self.book_source = book_source
        self.chapters_to_skip = chapters_to_skip
        self.book_content = epub.read_epub(self.book_source)
        self.chapters = self._get_chapters()

    def _get_chapters(self):
        print("Getting chapters from the book")
        chapters = self._get_chapters_from_epub(self.book_content)
        with Pool() as p:
            chapters['chapters'] = p.starmap(self._get_chapter_content, [(chapter, self.book_content, index, chapters['chapters']) for index, chapter in enumerate(chapters['chapters'])])
        return chapters
    
    def _get_chapters_from_epub(self, book):
        chapters = []
        for index, a in enumerate(book.toc):
            if isinstance(a, ebooklib.epub.Link):
                self._add_chapter(chapters, a, index)
            elif isinstance(a, tuple):
                # Handle the case where 'a' is a tuple
                section, links = a
                for link in links:
                    self._add_chapter(chapters, link, index)
        return {'chapters': chapters}

    def _add_chapter(self, chapters, link, index):
        if link.title.lower() not in self.chapters_to_skip:
            chapter = {}
            chapter['id'] = link.uid if link.uid else f'chapter_{index}'
            chapter['title'] = link.title
            chapter['href'] = link.href
            chapters.append(chapter)
    
    def _get_chapter_content(self, chapter, book, index, chapters):
    
        href_base, _, href_locator = chapter['href'].partition('#')
        next_chapter_href_locator = ""
        if index < len(chapters) - 1:
            next_chapter = chapters[index + 1]
            _, _, next_chapter_href_locator = next_chapter['href'].partition('#')

        item = book.get_item_with_href(href_base)
        if item:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            if href_locator:
                element = soup.find(id=href_locator)
                content = []
                if element:
                    next_elements = [element] + list(element.find_all_next())
                    
                    for next_element in next_elements:
                        if next_chapter_href_locator != "" and next_element.get('id') == next_chapter_href_locator:
                            break
                        if next_element.string:
                            content.append(next_element.string)
                    chapter['content'] = ' '.join(content)
                else:
                    chapter['content'] = ''
            else:
                chapter['content'] = soup.get_text()

        return chapter
    