from pypdf import PdfReader, PdfWriter

def get_chapters_from_pdf(input_pdf_path):
    # Load the PDF
    reader = PdfReader(input_pdf_path)
    pages = reader.pages
    # Extract the table of contents
    toc = reader.outline
    chapters = []
    # store the id, title, start page and end page of each chapter and include nested chapters
    process_toc(toc, reader, chapters)
    return {'chapters': chapters, 'reader': reader}

def process_toc(toc, reader, chapters):
    for i, item in enumerate(toc):
        if isinstance(item, list):
            # If the item is a list, it means it's a nested chapter. Process it recursively.
            process_toc(item, reader, chapters)
            continue
        chapter = {}
        chapter['id'] = len(chapters)  # Use the current length of chapters as id
        chapter['title'] = item.title
        start_page = item.page.get_object()
        # Get the start page number
        for i in range(len(reader.pages)):
            if reader.pages[i] == start_page:
                start_page_number = i
                break

        # Assume the end page of a chapter is the start page of the next chapter minus one
        if i + 1 < len(toc) and not isinstance(toc[i + 1], list):
            end_page = toc[i + 1].page.get_object()
            for i in range(len(reader.pages)):
                if reader.pages[i] == end_page:
                    end_page_number = i - 1
                    break
        else:
            # For the last chapter, use the total number of pages as the end page
            end_page_number = len(reader.pages) - 1

        chapter['start_page'] = start_page_number
        chapter['end_page'] = end_page_number
        chapters.append(chapter)

# function to get text for the selected chapters
def get_text_for_selected_chapters_pdf(chapters, reader):
    chapters_with_text = []
    for chapter in chapters:
        text = ''
        for i in range(chapter['start_page'], chapter['end_page'] + 1):
            text += reader.pages[i].extract_text()
        chapters_with_text.append({'id': chapter['id'], 'title': chapter['title'], 'content': text, 'start_page': chapter['start_page'], 'end_page': chapter['end_page']})
    return chapters_with_text