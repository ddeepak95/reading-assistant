from setuptools import setup, find_packages

setup(
    name="book_summarizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'tinydb',
        'beautifulsoup4',
        'ebooklib',
        'pydantic-ai',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for processing ebooks and generating AI-powered summaries",
    url="https://github.com/yourusername/book_summarizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 