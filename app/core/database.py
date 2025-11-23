
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load .env from current directory for portability
load_dotenv()

url = os.getenv("MONGODB_CONNECTION")
client = MongoClient(url)

try:
    client.admin.command('ping')
    print("✅ Connected to MongoDB!")
except Exception as e:
    print("❌ Could not connect to MongoDB:", e)

