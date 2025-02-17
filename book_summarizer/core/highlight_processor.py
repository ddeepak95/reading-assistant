from bs4 import BeautifulSoup
from copy import deepcopy
from typing import List, Dict
from tinydb import TinyDB, Query

class KindleHighlightParser:
    def __init__(self, html_path: str):
        """
        Initialize the parser with the path to the Kindle highlights HTML file.
        
        Args:
            html_path: Path to the Kindle highlights HTML file
        """
        self.html_path = html_path
        with open(self.html_path, 'r', encoding='utf-8') as f:
            self.soup = BeautifulSoup(f, 'html.parser')
        self.highlights = self.find_chapter_titles_and_highlights()

    def find_chapter_titles_and_highlights(self) -> List[Dict]:
        """Parse the Kindle highlights HTML file and extract highlights."""
        body = self.soup.find('body')
        elements = body.find_all(attrs={"class": ["sectionHeading", "noteText"]})
        result = []
        
        for element in elements:
            chapter = {}
            if element.get('class') == ['sectionHeading']:
                chapter['title'] = element.text.strip()
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

class HighlightProcessor:
    def __init__(self, highlights_db: TinyDB):
        """
        Initialize the highlight processor.
        
        Args:
            highlights_db: TinyDB instance for storing highlights
        """
        self.highlights_db = highlights_db
        self.Item = Query()

    def print_stats(self, doc_id: str) -> None:
        """
        Print statistics about the number of chapters and highlights.
        
        Args:
            doc_id: ID of the document
        """
        doc_highlights = self.highlights_db.search(self.Item.uid == doc_id)
        if not doc_highlights:
            print("No highlights found for document")
            return
            
        highlights = doc_highlights[0].get('kindle_highlights', [])
        num_chapters = len(highlights)
        total_highlights = sum(len(chapter['highlights']) for chapter in highlights)
        
        print(f"Number of chapters: {num_chapters}")
        print(f"Total number of highlights: {total_highlights}")

    def process_highlights(self, highlights_path: str, doc_id: str) -> None:
        """
        Process highlights from a Kindle highlights HTML file and store them in the database.
        
        Args:
            highlights_path: Path to the Kindle highlights HTML file
            doc_id: ID of the document the highlights belong to
        """
        parser = KindleHighlightParser(highlights_path)
        
        # Convert to database format
        kindle_highlights = []
        for chapter in parser.highlights:
            kindle_highlights.append({
                'chapter': chapter['title'],
                'highlights': chapter['highlights']
            })
        
        # Store highlights in database
        self.highlights_db.upsert(
            {
                'uid': doc_id,
                'kindle_highlights': kindle_highlights
            },
            self.Item.uid == doc_id
        )

        self.print_stats(doc_id)



    def find_highlights_for_chapter(self, chapter_title: str, doc_id: str) -> List[str]:
        """
        Find all highlights for a specific chapter.
        
        Args:
            chapter_title: Title of the chapter
            doc_id: ID of the document
            
        Returns:
            List of highlight texts for the chapter
        """
        doc_highlights = self.highlights_db.search(self.Item.uid == doc_id)
        if not doc_highlights:
            return []
            
        highlights = doc_highlights[0].get('kindle_highlights', [])
        chapter_highlights = []
        for h in highlights:
            if h['chapter'].lower() == chapter_title.lower():
                chapter_highlights.extend(h['highlights'])
        
        return chapter_highlights