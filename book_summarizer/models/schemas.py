from typing import List, Optional
from pydantic import BaseModel, Field

class InfoPointer(BaseModel):
    pointer: str = Field(description="An informative point focusing on a particular aspect of the chapter")
    related_quote_highlighted_by_reader: str | None = Field(description="A related quote to the pointer highlighted by the reader. Return None if there is no related quote.")

class InfoPoints(BaseModel):
    subtitle: str = Field(description="Subtitle that describes the theme of the info points")
    pointers: List[InfoPointer]

class ChapterSummary(BaseModel):
    chapter_descriptor: str = Field(description="A phrase that describes the chapter well")
    chapter_summary: str = Field(description="A succint summary of the chapter")
    info_points: List[InfoPoints]
    mermaid_graph: str = Field(description="Code for mermaid flowchart that depicts the chapter")

class Book(BaseModel):
    uid: str
    name: str
    folder: str
    toc: Optional[List[dict]] = None
    children_file_details: Optional[List[dict]] = None 