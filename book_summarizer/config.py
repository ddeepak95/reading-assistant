import os
from pathlib import Path

class Config:
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    
    # Database paths
    DB_DIR = DATA_DIR / "db"
    MAIN_DB_PATH = DB_DIR / "main.json"
    HIGHLIGHTS_DB_PATH = DB_DIR / "kindle_highlights.json"
    
    # Working directories
    WORKING_BASE_DIR = DATA_DIR / "srcs"
    
    # Create necessary directories
    @classmethod
    def initialize(cls):
        """Create all necessary directories if they don't exist."""
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.DB_DIR, exist_ok=True)
        os.makedirs(cls.WORKING_BASE_DIR, exist_ok=True) 