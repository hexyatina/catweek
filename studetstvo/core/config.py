from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_LOCAL = os.getenv('DATABASE_LOCAL')
DATABASE_REMOTE = os.getenv('DATABASE_REMOTE')