import os
from process_data import all_splits
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

google_api_key = os.environ["GEMINI_API_KEY"]

# Create embedded function
embedding_func = GoogleGenerativeAIEmbeddings(model="models/embedding-001", 
                                              google_api_key=google_api_key)

# Directory where the vector store is persisted
persist_directory = 'chromadb'

# Reload existing Chroma vector store
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding_func)

# Add new documents
vectordb.add_documents(all_splits)