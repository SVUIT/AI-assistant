import os 
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

google_api_key = os.environ["GEMINI_API_KEY"]

## Load data from directory
loader = DirectoryLoader("reference/", show_progress=True , use_multithreading=True)
docs = loader.load()

## split data into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1300, chunk_overlap=200 
)
all_splits = text_splitter.split_documents(docs)