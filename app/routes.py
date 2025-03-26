from fastapi import APIRouter, HTTPException
from app.clustering import cluster_files
from app.db import get_file_names
from llama_index.llms.gemini import Gemini
import google.generativeai as genai
from llama_index.core import Settings
from dotenv import load_dotenv
import os
load_dotenv()
router = APIRouter()
gemini_key = MONGO_URI = os.getenv("MONGO_URI")

genai.configure(api_key=gemini_key)
llm = Gemini(model_name="models/gemini-1.5-flash")
Settings.llm = llm

@router.get("/cluster")
async def run_clustering():
    """Runs the clustering process and returns the clustered data."""
    try:
        clustered_data = await cluster_files(llm)
        return {"clusters": clustered_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/files")
async def fetch_file_names():
    
    """API endpoint to get distinct file names from MongoDB."""
    try:
        file_names = await get_file_names()
        return {"file_names": file_names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
