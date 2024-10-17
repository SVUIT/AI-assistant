import os

from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings


#create vectorstore from qdrant
api_key_qdrant = os.environ["QDRANT_API_KEY"]
url = os.environ["URL_QDRANT"]
collection_name = "dsc_data"
embedding_function = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vectorstore = QdrantVectorStore.from_existing_collection(
    collection_name="dsc_data",
    embedding=embedding_function,
    url=url,
    api_key=api_key_qdrant,
)

#create retriever
retriever_llm = vectorstore.as_retriever(search_type="mmr",search_kwargs={"k": 7})

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
google_api_key = os.environ["GEMINI_API_KEY"]


output_parser = StrOutputParser()

llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash", google_api_key = google_api_key , temperature = 0.2,
                             top_p = 0.9, top_k = 1, max_output_tokens = 2000)

# Create question maker

def contextualized_question(input: dict):
    if input.get("chat_history"):
        return question_chain
    else:
        return input["question"]

instruction_to_system = """
Given a chat history and the latest user question 
which might reference context in the chat history, formulate a standalone question 
which can be understood without the chat history. Do NOT answer the question, 
just reformulate it if needed and otherwise return it as is.
"""

question_maker_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", instruction_to_system),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)


question_chain = question_maker_prompt | llm | StrOutputParser()

# build the prompt for the question and answer
qa_system_prompt = """You are an VietNamese-English assistant for question-answering tasks related courses of Information Technology (UIT), Vietnam National University, Ho Chi Minh City. \
  Please use the following pieces of context{context} to generate the question at the end.
  If you do not know the answer, please do not answer from your knowledge base and say that sorry, I do not know it. Do not recommend anything.
  Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.\
  However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
  strike a friendly and converstional tone. \
  Output result in Vietnamese.\
  If the passage is irrelevant to the answer, you may ignore it.
  QUESTION: {question}
  """
qa_prompt = ChatPromptTemplate.from_messages(
    [
        
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "Du lịch Việt Nam nên đi đâu?"),
        ("ai", "Xin lỗi, Tôi không được thiết kế để trả lời câu hỏi này. Tôi chỉ có thể trả lời các câu hỏi liên quan đến công nghệ thông tin, mạng máy tính, UIT"),
        ("human","Bạn có biết Doraemon không?"),
        ("ai","Xin lỗi, Tôi không được thiết kế để trả lời câu hỏi này. Tôi chỉ có thể trả lời các câu hỏi liên quan đến công nghệ thông tin, mạng máy tính, UIT"),
        ("human", "Please answer the question based the context. If you don't know the question, just say sorry, i don't know"),
        ("ai", "Ok, I won't use my based knowledge"),
        ("human", "Bạn có thể trả lời các câu hỏi về chủ đề gì?"),
        ("ai", "Tôi chỉ có thể trả lời các câu hỏi dựa trên kiến thức cua các môn học của khoa mạng máy tính và truyền thông, Trường đại học Công Nghệ Thông Tin(UIT)."),
        ("human", "{question}"),
        
    ]
)


retriever_chain = RunnablePassthrough.assign(
        context=contextualized_question | retriever_llm
    )

## create  main chain that produces the final answer
rag_chain = (
    retriever_chain
    | qa_prompt
    | llm
)