import os
from load_data import vectordb
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

google_api_key = os.environ["GEMINI_API_KEY"]


output_parser = StrOutputParser()

llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash", google_api_key = google_api_key , temperature = 0.5,
                             top_p = 0.95, top_k = 64, max_output_tokens = 8192)

# create retriever
retriever = vectordb.as_retriever(search_kwargs={"k": 10})

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
qa_system_prompt = """You are a helpful and informative bot that answers questions using text from the reference passage included below. \
  You can translate questions to English and Vietnamese to find the answer. But the answer must be translated to English. \
  All documents are from courses at the University of Information Technology (UIT), Vietnam National University, Ho Chi Minh City. \
  You can use the course codes, Vietnamese course names, English course names in the file `courses_list.docx` to find information more easily. \
  Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
  However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
  strike a friendly and converstional tone. \
  If the passage is irrelevant to the answer, you may ignore it.
  QUESTION: '{question}'
  PASSAGE: '{context}'
  ANSWER:"""
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)


retriever_chain = RunnablePassthrough.assign(
        context=contextualized_question | retriever 
    )

## create main chain that produces the final answer
rag_chain = (
    retriever_chain
    | qa_prompt
    | llm
)
