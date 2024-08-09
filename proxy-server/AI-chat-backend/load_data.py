from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os

google_api_key = os.getenv("GEMINI_API_KEY")

## Load data from chromadb 
persist_directory = 'chromadb'
embedding_func = GoogleGenerativeAIEmbeddings(model = "models/embedding-001" , google_api_key = google_api_key)
vectordb = Chroma(persist_directory=persist_directory, 
                  embedding_function=embedding_func)

