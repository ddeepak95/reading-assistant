import os
import requests
from dotenv import load_dotenv
load_dotenv()

class NotionPage:
    TOKEN = os.getenv("NOTION_TOKEN_KEY")

    def __init__(self, parent_page_id, title):
        self.headers = {
            'Authorization': f'Bearer {self.TOKEN}',
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        self.parent_page_id = parent_page_id
        self.title = title
        self.page_id = None
        self.page_url = None
        self.create_page = self.create_page(self.parent_page_id, self.title)
        
        

    def create_page(self, parent_page_id, title):
        print("Creating Notion Page: " + title)
        url = "https://api.notion.com/v1/pages/"
        create_page_body = {
            "parent": {"page_id": parent_page_id},
            "properties": {
                "title": [
                    {
                        "type": "text",
                        "text": {"content": title}
                    }
                ]
            },
        }

        response = requests.request("POST", url, headers=self.headers, json=create_page_body)
        response_json = response.json()
        if response.status_code == 200:
            self.page_id = response_json['id']
            self.page_url = response_json['url']
            return response_json
        else:
            print(f"Failed to create page: {response_json}")
            return None

    def add_chapter_to_page(self, page_id, chapter_summary, chapter_highlights):
        print("Adding Chapter to Notion Page: " + chapter_summary['title'])
        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        formatted_chapter = self.format_chapter_for_notion(chapter_summary, chapter_highlights)

        response = requests.request("PATCH", url, headers=self.headers, json={"children": formatted_chapter})
        response_json = response.json()
        return response_json

    @staticmethod
    def format_chapter_for_notion(chapter_summary, chapter_highlights):
        children = []


        short_summary = {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": chapter_summary['summary']['overall_summary'],
                            "link": None
                        }
                    }
                ]
            }
        }
        children.append(short_summary)

        for summary in chapter_summary['summary']['summary_pointers']:
            subtitle = {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": summary['subtitle'],
                                "link": None
                            }
                        }
                    ]
                }
            }
            children.append(subtitle)
            if summary['relevant_highlights'] != []:
                for highlightIndex in summary['relevant_highlights']:
                    highlight = chapter_highlights[int(highlightIndex)]
                    formatted_highlight = {
                        "object": "block",
                        "type": "callout",
                        "callout": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": highlight,
                                        "link": None
                                    }
                                }
                            ],
                            "icon": {
                                "type": "emoji",
                                "emoji": "🔖"
                            },
                            "color": "yellow_background"
                        }
                    }
                    children.append(formatted_highlight)

            for pointer in summary['ideas']:
                formatted_pointer = {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": pointer,
                                    "link": None
                                }
                            }
                        ]
                    }
                }
                children.append(formatted_pointer)

                    

        if chapter_highlights != []:
            callouts =[]
            for highlight in chapter_highlights:
                formatted_highlight = {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": highlight,
                                    "link": None
                                }
                            }
                        ],
                        "icon": {
                            "type": "emoji",
                            "emoji": "🔖"
                        },
                        "color": "yellow_background"
                    }
                }
                callouts.append(formatted_highlight)

            highlights_header = {
                "object": "block",
                "type": "heading_2",
                "has_children": True,
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "All Highlights",
                                "link": None
                            }
                        }
                    ],
                    "is_toggleable": True,
                    "children": callouts
                },
                
            }
            children.append(highlights_header)


                                  

        formatted_chapter = {
            "object": "block",
            "type": "heading_1",
            "has_children": True,
            "heading_1": {
                "rich_text": [{
                "type": "text",
                "text": {"content": chapter_summary['title'],},
                "annotations": {
                    "bold": True
                },
                }],
                "is_toggleable": True,
                "children": children
            }
        }
        divider = {
            "object": "block",
            "type": "divider",
            "divider": {}
        }
        return [formatted_chapter, divider]

    def create_page_and_add_chapters(self, parent_page_id, title, content):
        self.create_page(parent_page_id, title)
        for chapter in content:
            self.add_chapter_to_page(self.page_id, chapter)
        print("Page Created and Chapters Added")
        print(f"Page URL: {self.page_url}")
        