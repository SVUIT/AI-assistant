import os
from create_reader import reader
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient


# get qdrant client and embedding_function

api_key_qdrant = os.environ["QDRANT_API_KEY"]
url = os.environ["URL_QDRANT"]
collection_name = "dsc_data"
client = QdrantClient(url=url,api_key=api_key_qdrant)
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# print(reader.model, reader)

def get_relevant_plot(question: str, top_k: int) -> List[str]:
    """
    Get the relevant plot for a given question

    Args:
        question (str): What do we want to know?
        top_k (int): Top K results to return

    Returns:
        context (List[str]):
    """
    try:
        encoded_query = embedding_function.embed_query(question) # generate embeddings for the question

        result = client.query_points(
            collection_name=collection_name,
            query=encoded_query,
            limit=top_k,
        ).points  # search qdrant collection for context passage with the answer

        
        context = [
            [x.payload.get("metadata", "No Metadata"), x.payload.get("page_content", "No Content")] for x in result
        ]  # extract title and payload from result
        # print(context)
        return context

    except Exception as e:
        print({e})

def extract_answer(question: str, context: List[str]):
    """
    Extract the answer from the context for a given question

    Args:
        question (str): _description_
        context (list[str]): _description_
    """
    results = []
    for c in context:
        # feed the reader the question and contexts to extract answers
        answer = reader(question=question, context=c[1])

        # add the context to answer dict for printing both together, we print only first 500 characters of plot
        answer["title"] = c[0]
        results.append(answer)

    # sort the result based on the score from reader model
    sum=0
    sorted_result = sorted(results, key=lambda x: x["score"], reverse=True)
    for i in range(len(sorted_result)):
        print(f"{i+1}", end=" ")
        sum += sorted_result[i]["score"]
        print(
            "Answer: ",
            sorted_result[i]["answer"],
            "\n  Title: ",
            sorted_result[i]["title"],
            "\n  score: ",
            sorted_result[i]["score"],
        )
    print(sum)
    return sum