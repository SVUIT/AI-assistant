from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load data form directory 
loader = DirectoryLoader("folder", show_progress=True , use_multithreading=True)
doc = loader.load()

# Split data to chunk
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=550, chunk_overlap=100 
)
docs = text_splitter.split_documents(doc)