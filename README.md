# Reading Assistant

The application generates chapter-wise summaries of an ePub book and adds them to a Notion page, aligning them with the corresponding highlights made in Kindle. It is not intended to replace book reading but to help you develop a personal knowledge base for easy retrieval and recall. The application uses the OpenAI API to generate summaries and the Notion API to add both the summaries and highlights to a Notion page.

## Features

- Generate chapter-wise summaries of an ebook using AI
- Get chapter-wise highlights made in Kindle
- Adds the summary and highlights to a Notion page

Here's a sample Notion page created by the application:
[https://ddeepak95.notion.site/Why-Buddhism-is-True-3266cca15dff4118afc79932e812c041?pvs=4](https://ddeepak95.notion.site/Why-Buddhism-is-True-3266cca15dff4118afc79932e812c041?pvs=4)

### How to get Kindle highlights file

- Use the Kindle app on your computer to export the highlights of the book as a HTML file.

## Setting up

- Setup a virtual environment by running `python -m venv venv` in the project directory.
- Install the required Python packages by running `pip install -r requirements.txt`.
- Set up your environment variables in a `.env` file. You need to provide the following:

  ```
  OPENAI_API_KEY = "your_openai_api_key"
  NOTION_TOKEN_KEY = "your_notion_token_key"
  NOTION_PARENT_PAGE_ID = "your_notion_parent_page_id"
  ```

  - Refer to the [Notion documentation](https://developers.notion.com/docs/authorization#what-is-an-internal-integration) for obtaining the token. Internal integration is enough for personal use of this application.
  - `NOTION_PARENT_PAGE_ID` is the ID of the Notion page where you want to create the book pages. You can find this ID in the URL of the page.
  - Get the OpenAI API key from the OpenAI dashboard.

## Usage

- In `app.py`, specify the path to your epub file and the HTML file containing the highlights. Also, provide the title of the book and a list of chapters to skip.
- Run the application using python app.py.
- The application will start a local server and provide a URL. Visit this URL to preview the loaded epub and highlights content. Make sure the content is loaded properly before proceeding with the application. If the content is not loaded properly, you may need to adjust the HTML content or the epub file to ensure proper extraction of the content and highlights
- If the content and highlights are loaded properly, press Ctrl+C to stop the server and proceed with the application.
- The application will then generate a summary of the book content and add it to the specified Notion page.

## Known Issues

- The application may not work properly with all epub files. Some epub files may have complex structures that are not supported by the current implementation. If you encounter any issues with the epub file, you may need to adjust the code to handle the specific structure of the epub file.
- The application may not work properly with all HTML files containing highlights. Some HTML files may have complex structures that are not supported by the current implementation. If you encounter any issues with the HTML file, you may need to adjust the code to handle the specific structure of the HTML file.

Please feel free to open an issue if you encounter any problems or have any suggestions for improvement. Also, feel free to contribute to the project by submitting a pull request.

## What's next?

Based on the time available, I might add the following features to the application:

- Support for more ebook formats
- Support for versatile highlight formats
- Develop a frontend for the application

## Note

This application uses OpenAI for generating summaries, so make sure you have enough API credits before running the application.
