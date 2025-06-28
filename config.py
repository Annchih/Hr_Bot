from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
HR_ID = set(map(int, getenv("HR_ID", "").split(",")))
ADMINS = set(map(int, getenv("ADMINS", "").split(",")))

