chat_history = []
from langchain_core.messages import HumanMessage
from create_chain import rag_chain
from get_relevant_score import get_relevant_plot, extract_answer 



question = "Hệ điều hành là gì"
context = get_relevant_plot(question, top_k=3)
score = extract_answer(question, context)
if ( score < 0.1):
    print("Tôi xin lỗi, tôi không có đủ thông tin để trả lời câu hỏi này")
else:
    ai_msg = rag_chain.invoke({"question": question, "chat_history": chat_history , "topic": "UIT, internet and information technology"})
            
        # Update chat history with the new messages
    chat_history.extend([HumanMessage(content=question), ai_msg])
    print(ai_msg.content)