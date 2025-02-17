# Features

- Ability to view the list of books in the main_db and kindle_highlights DB
- Load the book and highlights
  - From user, get the epub file path and highlights file path (if available). There should be provisions to add highlights later too
  - Create an unique book_id for the book
  - Save the source files to the working folders
    - Extract the files from the epub to the working folder for easy processing
  - Create an entry in the main db for the new book
  - Get the ToC of the book from the epub
    - Update the ToC href based on the files extracted from the epub [yet to be implemented]
  - Save the ToC of the book to the entry in the main db
  - Save the Highlights to the Kindle Highlights DB if the highlights file is available
- Generating the chapter summaries from the book
  - Get the md file path where the chapter summary has to be saved
  - Get the book_id from the user for which the summary has to be generated
    - Check if the book if there in the db. If not, ask the user to load the book to the system
  - Get the relevant ToC and Highlights(if available) from the dbs
  - For the items in the ToC, get the file and use the agent to the summary and store in the given md file
