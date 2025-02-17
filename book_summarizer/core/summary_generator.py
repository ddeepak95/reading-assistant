from bs4 import BeautifulSoup
from typing import List, Optional
from pydantic_ai import Agent
from ..models.schemas import ChapterSummary

class SummaryGenerator:
    def __init__(self):
        """
        Initialize the summary generator.
        
        Args:
            openai_api_key: OpenAI API key for GPT access
        """
        self.agent = Agent('openai:gpt-4o', result_type=ChapterSummary)

    def extract_clean_content(self, html_path: str) -> Optional[str]:
        """
        Extract clean text content from an HTML file.
        
        Args:
            html_path: Path to the HTML file
            
        Returns:
            Clean text content or None if file is empty
        """
        with open(html_path, 'rb') as f:
            content = f.read()
            if content:
                soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')
                return soup.get_text()
        return None

    def generate_chapter_summary(
        self, 
        chapter_content: str, 
        highlights: List[str]
    ) -> ChapterSummary:
        """
        Generate a chapter summary using the AI agent.
        
        Args:
            chapter_content: The text content of the chapter
            highlights: List of highlights for the chapter
            
        Returns:
            ChapterSummary object containing the generated summary
        """

        system_message = """You are a skilled book summarizer who excels at:
        1. Identifying and synthesizing main themes
        2. Creating clear, structured summaries
        3. Connecting reader highlights to key points
        4. Generating intuitive flowcharts
        
        Your response must follow the ChapterSummary schema with these fields:
        - info_points: List of key points that support the themes
        - related_quote_highlighted_by_reader: Optional quote highlighted by the reader related to the point. Strictly return None if there is no related quote.
        - brief_summary: A concise summary of the chapter's essence
        - mermaid_graph: A mermaid flowchart of the chapter's concepts. Don't use quote marks in the flowchart.
        """

        prompt = """
        Below is a content of a chapter from a book along with quotes highlighted by the reader.
        
        Book Content:
        {context_str}
        
        Quotes highlighted by the reader:
        {quotes}
              
        Summary:
        """

        agent = Agent('openai:gpt-4o', system_prompt=system_message, result_type=ChapterSummary)
        
        query = prompt.format(
            context_str=chapter_content, 
            quotes='\n'.join(highlights)
        )

        result = agent.run_sync(query)
        return result

