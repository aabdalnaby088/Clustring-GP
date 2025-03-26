import os
import asyncio
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# Get MongoDB URI from .env
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is missing! Check your .env file.")

# MongoDB Connection
client = MongoClient(MONGO_URI)
database = client["test"]  # Use your actual database name
files_collection = database["datas"]
clusters_collection = database["clusters"]

async def get_file_names():
    """Fetch distinct file names from the 'datas' collection."""
    try:
        data =  files_collection.distinct("name")
        if not data:
            print(" No data found in 'datas' collection.")
        return data
    except Exception as e:
        print(f"Error fetching file names: {e}")
        return []


async def save_clusters_to_db(clusters):
    """Save the clustered categories to the MongoDB database."""
    try:
        clusters_collection.delete_many({})
        clusters_collection.insert_many(clusters)
        print("✅ Clusters successfully saved to MongoDB.")
    except Exception as e:
        print(f" Error saving clusters to DB: {e}")