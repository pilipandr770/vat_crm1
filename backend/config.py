import os, dotenv, pathlib
BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
dotenv.load_dotenv(BASE_DIR/".env", override=True)
class settings:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL","sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY","dev")
