import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:

    USER : str = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    SERVER : str = os.getenv("SERVER","localhost")
    PORT : str = os.getenv("PORT",3306)
    DB : str = os.getenv("DB","first_db")
    DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}"

settings = Settings()