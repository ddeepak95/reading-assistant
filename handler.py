from epub_functions import Book
from openai_functions import get_chat_completion
from notion_functions import NotionPage
from html_functions import KindleHTMLParser, create_html
from flask import Flask
import json
import os
import shutil
import jsonschema

class Summarizer:
    def __init__(self, summary_instructions):
        self.summary_instructions = summary_instructions

    def validate_summary_format(self, summary, highlights):
        schema = {
            "type": "object",
            "properties": {
                "summary_pointers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "subtitle": {"type": "string"},
                            "ideas": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "relevant_highlights": {
                                "type": "array",
                                "items": {"type": "integer"}
                            }
                        },
                        "required": ["subtitle", "ideas", "relevant_highlights"]
                    }
                },
                "overall_summary": {"type": "string"}
            },
            "required": ["summary_pointers", "overall_summary"]
        }

        try:
            jsonschema.validate(instance=summary, schema=schema)
            for summary in summary['summary_pointers']:
                if any(highlightIndex >= len(highlights) for highlightIndex in summary['relevant_highlights']):
                    print("One or more relevant highlights are out of range.")
                    return False           
            return True
        except jsonschema.exceptions.ValidationError as err:
            print(err)
            return False

    def get_summary(self, chapter, highlights):
        print(f"Summarizing chapter: {chapter['title']}")
        main_instructions = 'You are an expert book summariser. Summarise only the text in the user input. Do not add any new information. Do not include your opinion. The ideas in the summary could include explanations, anedoctes, concepts, or any other information that is relevant to the chapter. The reader should get a good understanding of the chapter by reading the summary.'
        additional_instructions = 'The input is a json with chapter content and highlights annotated by a reader. Summarize the chapter content and match the highlights to the relevant ideas in the summary. The return json should contain the summary ideas and the index values of the highlights. One highlight should not be matched to multiple ideas and all the highlights should be matched to atleast one idea. It is ok to return an empty array if there are no matching highlights or no highlights in the input. The schema should be as follows {"summary_pointers" :[{"subtitle":"Theme", "ideas": ["Sentence explaining the idea 1", "Sentence explaining the idea 2", ...],"relevant_highlights":[relevant_highlight_index_as_int,...]},{"subtitle":"Theme", "ideas": ["Sentence explaining the idea 1", "Sentence explaining the idea 2", "Sentence explaining the idea 3", ...], "relevant_highlights":[]}]},"overall_summary": "Overall suummary of the chapter in less than 100 words."}'

        input = {
            "chapter_content": chapter['content'],
            "highlights": highlights
        }

        input_string = json.dumps(input)
       
        json_summary = self.get_valid_summary(main_instructions, additional_instructions, input_string, highlights)
        return {'id': chapter['id'], 'title': chapter['title'], 'summary': json_summary}
    
    def get_valid_summary(self, main_instructions, additional_instructions, input_string, highlights):
        while True:
            summary = get_chat_completion(main_instructions + " " + self.summary_instructions + " " + additional_instructions, input_string)
            if self.validate_summary_format(json.loads(summary), highlights):
                return json.loads(summary)
            print("The summary format is not valid. Please try again.")     


class Application:
    def __init__(self, book_source, html_source, summary_instructions, notion_parent_page_id, book_title, chapters_to_skip):
        """
        book_source: Path to the epub file
        html_source: Path to the html file with highlights
        summary_instructions: Instructions to the AI summarizer
        notion_parent_page_id: The id of the Notion parent page
        book_title: The title of the book
        chapters_to_skip: List of chapters to skip while summarizing and adding to Notion
        """
        
        self.book_title = book_title
        self.notion_parent_page_id = notion_parent_page_id
        self.book = Book(book_source, chapters_to_skip)
        self.chapters = self.book.chapters['chapters']
        self.htmlHightlights = KindleHTMLParser(html_source).highlights
        self.notion_page = None
        self.instructions = summary_instructions
        self.temp_server_folder = './loaded_content_preview'

    
    def start(self):
        server_directory = os.path.join(self.temp_server_folder, '')
        create_html(server_directory, self.chapters, self.htmlHightlights)
        self.start_server()
        print("**")
        # ANSI escape codes for styling
        GREEN_BOLD = "\033[1;32m"
        RESET = "\033[0m"
        # Text to display
        text = "Do you want to proceed with the AI summary and adding to Notion? (y/n): "
        # Print the styled text
        print(f"{GREEN_BOLD}{text}{RESET}")
        # Get user input
        proceed = input()
        if proceed.lower() == 'y':
            self.destroy_html()
            self.notion_page = NotionPage(self.notion_parent_page_id, self.book_title)       
            for chapter in self.chapters:
                highlights = self.get_highlights(chapter)
                summary = self.get_summary(chapter, highlights)
                self.add_summary_and_highlights_to_notion(summary, highlights)
        else:
            self.destroy_html()
            print("Exiting without adding to Notion")



    def start_server(self):
        app = Flask(__name__, static_folder=self.temp_server_folder)
        host = '127.0.0.1'
        port = 5000
        serving_url = f"http://{host}:{port}"
        @app.route('/')
        def home():     
            return app.send_static_file('index.html')
        print("**")
        print("Check if the text from the chapters in the epub file and the highlights from the html file are loaded properly before proceeding with the application to ensure that the AI API credits are not wasted.")
        print("\033[92m" + f"Preview the loaded epub content and highlights at {serving_url}" + "\033[0m")
        print("**")
        print("Press Ctrl+C to stop the server and proceed with the application")
        print("**")
        app.run(host=host, port=port)

    def destroy_html(self):
        shutil.rmtree(self.temp_server_folder)


    def get_summary(self, chapter, highlights):
        summarizer = Summarizer(self.instructions)
        summary = summarizer.get_summary(chapter, highlights)
        return summary
    
    def get_highlights(self, chapter):
        for highlight in self.htmlHightlights:
            if highlight['title'] == chapter['title']:
                return highlight['highlights']
        return []
    
    def add_summary_and_highlights_to_notion(self, summary, highlights):
        self.notion_page.add_chapter_to_page(self.notion_page.page_id, summary, highlights)



    



