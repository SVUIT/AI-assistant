import os
from langchain_qdrant import QdrantVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import chain
from langchain_core.documents import Document
from typing import List

#create vectorstore from qdrant
api_key_qdrant = os.environ["QDRANT_API_KEY"]
url = os.environ["URL_QDRANT"]
collection_name = "dsc_data"
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
vectorstore = QdrantVectorStore.from_existing_collection(
    collection_name=collection_name,
    embedding=embedding_function,
    url=url,
    api_key=api_key_qdrant,
)

#create retriever
@chain
def retriever(query: str) -> List[Document]:
    docs, scores = zip(*vectorstore.similarity_search_with_score(query,30))
    for doc, score in zip(docs, scores):
        doc.metadata["score"] = score

    return docs

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
google_api_key = os.environ["GEMINI_API_KEY"]


output_parser = StrOutputParser()

llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash", google_api_key = google_api_key , temperature = 0.4,
                             top_p = 0.7, top_k = 10, max_output_tokens = 5000)

# create retriever
# retriever = vectorstore.as_retriever(search_type="similarity",search_kwargs={"k": 40})

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
# qa_system_prompt = """You are an VietNamese-English assistant for question-answering tasks related courses of Information Technology (UIT), Vietnam National University, Ho Chi Minh City. \
#   Please use the following pieces of context{context} to generate the question at the end.
#   You can 
#   If you do not know the answer, please do not answer from your knowledge base and say that sorry, I don't have information about it. Do not recommend anything.
#   Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.\
#   However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
#   strike a friendly and converstional tone. \
#   Output result in Vietnamese.\
#   If the passage is irrelevant to the answer, you may ignore it.
#   QUESTION: {question}
#   """
# qa_system_prompt = """Bạn là một trợ lý tiếng Việt - tiếng Anh cho các nhiệm vụ trả lời câu hỏi liên quan đến các môn học của Khoa Công Nghệ Thông Tin (UIT), Trường Đại Học Quốc Gia TP.HCM. \
# Bạn có quyền truy cập vào các đề thi của UIT và có thể cung cấp thông tin từ đó. \
# Xin vui lòng sử dụng các thông tin sau đây {context} trả lời câu hỏi và tìm kiếm đề thi hoặc tóm tắt nội dung của môn học. \
# Nếu bạn không biết câu trả lời, hãy nói rằng "Xin lỗi, tôi không có thông tin về điều này." và không đưa ra bất kỳ khuyến nghị nào. \
# Hãy đảm bảo trả lời trong một câu hoàn chỉnh, rõ ràng và đầy đủ, bao gồm tất cả thông tin nền cần thiết. \
# Bạn đang nói chuyện với một khán giả không có kiến thức kỹ thuật, vì vậy hãy giải thích các khái niệm phức tạp một cách đơn giản và giữ cho giọng điệu thân thiện, trò chuyện. \
# Kết quả đầu ra phải bằng tiếng Việt. \
# Nếu nội dung không liên quan đến câu hỏi, bạn có thể bỏ qua nó. \
# CÂU HỎI: {question}
# """
qa_system_prompt = """You are a Vietnamese-English assistant for question-answering tasks related to the courses of the Faculty of Information Technology (UIT), Vietnam National University, Ho Chi Minh City. \
You have access to the exam papers of UIT and can provide information from them. \
Please use the following pieces of information {context} to generate exam questions or summarize the content of the course. \
If you do not know the answer, please say, "Sorry, I don't have information about this." and do not make any recommendations. \
Make sure to respond in a complete, clear, and comprehensive sentence, including all necessary background information. \
You are speaking to a non-technical audience, so explain complex concepts simply and maintain a friendly, conversational tone. \
The output must be in Vietnamese. \
QUESTION: {question}
"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "Xin chào"),
        ("ai","Chào bạn, tôi là chatbot hỗ trợ trả lời câu hỏi của SVUIT. Tôi có thể giúp gì cho bạn?"),
        # ("human", "Du lịch Việt Nam nên đi đâu?"),
        # ("ai", "Xin lỗi, Tôi không được thiết kế để trả lời câu hỏi này. Tôi chỉ có thể trả lời các câu hỏi liên quan đến công nghệ thông tin, mạng máy tính, Trường đại học Công Nghệ Thông Tin(UIT)"),
        # ("human","Bạn có biết Doraemon không?"),
        # ("ai","Xin lỗi, Tôi không được thiết kế để trả lời câu hỏi này. Tôi chỉ có thể trả lời các câu hỏi liên quan đến công nghệ thông tin, mạng máy tính, Trường đại học Công Nghệ Thông Tin(UIT)"),
        # ("human", "Please answer the question based the context. If you don't know the question, just say sorry, i don't know"),
        # ("ai", "Ok, I won't use my based knowledge"),
        ("human", "Bạn có thể trả lời các câu hỏi về chủ đề gì?"),
        ("ai", "Tôi chỉ có thể trả lời các câu hỏi dựa trên kiến thức của các môn học của khoa mạng máy tính và truyền thông, Trường đại học Công Nghệ Thông Tin(UIT)."),
        # ("human", "Hay ke mot cau chuyen vui"),
        # ("ai","Xin loi, toi khong duoc lap trinh de ke chuyen. Toi la AI ho tro sinh vien UIT trong hoc tap"),
        ("human", "{question}"),
        
    ]
)


retriever_chain = RunnablePassthrough.assign(
        context=contextualized_question | retriever
    )

## create  main chain that produces the final answer
rag_chain = (
    retriever_chain
    | qa_prompt
    | llm
)