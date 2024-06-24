import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from multiprocessing import Pool

class Book:
    def __init__(self, book_source):
        self.book_source = book_source
        self.book_content = epub.read_epub(self.book_source)
        self.toc_details = self._get_toc_details()
        self.files_in_epub = self._get_files_in_epub()
    
    def _get_toc_details(self):
        toc = self.book_content.toc
        toc_details = []
        for item in toc:
            if isinstance(item, ebooklib.epub.Link):
                toc_item ={"type": "link", "href": item.href, "title": item.title, "uid": item.uid}

            elif isinstance(item, tuple) and isinstance(item[0], ebooklib.epub.Section):
                toc_item = {"type": "section", "title": item[0].title, "links": []}
                for link in item[1]:
                    toc_item["links"].append({"type": "link", "href": link.href, "title": link.title, "uid": link.uid})
            toc_details.append(toc_item)
        return toc_details

    def _get_files_in_epub(self):
        items = self.book_content.get_items()
        files = []
        for file_item in items:
            item_id = file_item.get_id()
            item_type = file_item.get_type()
            item_name = file_item.get_name()
            if item_type == 9:
                # get title of file by parsing html
                soup = BeautifulSoup(file_item.get_content(), 'html.parser')
                title = soup.title.string if soup.title else 'No Title'
                files.append({"file_id": item_id, "file_name": item_name, "title": title})
        return files
    