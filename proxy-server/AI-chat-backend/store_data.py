import os
from process_data import all_splits
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings


os.environ["GEMINI_API_KEY"] = "AIzaSyBm1d7G47E31LUG2UCDVPXlIVx-VakgySY"
google_api_key = os.environ["GEMINI_API_KEY"]


embedding_func = GoogleGenerativeAIEmbeddings(model = "models/embedding-001" , 
                                              google_api_key = google_api_key)

persist_directory = 'chromadb'
## store embedded data in chromadb
vectordb = Chroma.from_documents(documents=all_splits, 
                                 embedding=embedding_func,
                                 persist_directory=persist_directory)

vectordb = None