import os

from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain_huggingface import HuggingFaceEmbeddings
from tqdm.auto import tqdm
from load_data import docs

api_key_qdrant = os.environ["QDRANT_API_KEY"]
url = os.environ["URL_QDRANT"]
collection_name = "embedding_data"
client = QdrantClient(url=url,api_key=api_key_qdrant)

collections = client.get_collections()
# only create collection if it doesn't exist
if collection_name not in [c.name for c in collections.collections]:
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=384,
            distance=models.Distance.COSINE,
        ),
    )
collections = client.get_collections()
print(collections) 
# get embedding function
embedding_function = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
collection_vector_count = client.get_collection(collection_name=collection_name).points_count

batch_size = 64
for index in tqdm(range(0, len(docs), batch_size)):
    i_end = min(index + batch_size, len(docs))  
    batch = docs[index:i_end] 
    
    # embeddings
    emb = list(embedding_function.embed_documents([doc.page_content for doc in batch]))
    
    # prepare metadata and ID
    meta = [{'metadata': doc.metadata, 'page_content': doc.page_content} for doc in batch]
    ids = list(range(index+collection_vector_count, i_end+collection_vector_count))  

    # Upsert to Qdrant
    client.upsert(
        collection_name=collection_name,
        points=models.Batch(ids=ids, vectors=emb, payloads=meta),
    )

# check number of vector in collection
collection_vector_count = client.get_collection(collection_name=collection_name).points_count
print(f"Số lượng vector trong bộ sưu tập: {collection_vector_count}")