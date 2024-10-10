from flask import Flask, request, jsonify
from langchain_core.messages import HumanMessage
from create_chain import rag_chain
from get_relevant_score import get_relevant_plot, extract_answer 

# Initialize Flask app
app = Flask(__name__)

chat_history = []

@app.route('/')
def index():
    return "AI"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    print(data)
    question = data.get('question', '')
    print(question)
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        context = get_relevant_plot(question, top_k=3)
        score = extract_answer(question, context)
        if ( score < 0.1):
            return jsonify({'response': "Tôi xin lỗi, tôi không có đủ thông tin để trả lời câu hỏi này"})
        else:
            ai_msg = rag_chain.invoke({"question": question, "chat_history": chat_history , "topic": "UIT, internet and information technology"})
                    
                # Update chat history with the new messages
            chat_history.extend([HumanMessage(content=question), ai_msg])
            return jsonify({'response': ai_msg.content})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    # Run the Flask app on the specified host and port
    app.run(host='0.0.0.0', port=8000)