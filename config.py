import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    DATABASE = os.path.join(BASE_DIR, "instance/stock.db")

    DEBUG = True

    NEWS_API_KEY = os.getenv("NEWS_API_KEY")