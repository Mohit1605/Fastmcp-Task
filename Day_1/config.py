import os
from dotenv import load_dotenv

load_dotenv()

TRANSPORT = os.getenv("TRANSPORT", "stdio").lower()
PORT = int(os.getenv("PORT", 3000))