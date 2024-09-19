from flask import Flask, request, jsonify
from langchain_core.messages import HumanMessage
from create_chain import rag_chain

# Initialize Flask app
app = Flask(__name__)

# Initialize chat history
chat_history = []

@app.route('/')
def index():
    return "AI"

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    question = data.get('question', '')

    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        # Invoke the RAG chain with the provided question and chat history
        ai_msg = rag_chain.invoke({"question": question, "chat_history": chat_history})
        
        # Update chat history with the new messages
        chat_history.extend([HumanMessage(content=question), ai_msg])
        
        # Return the response from the AI
        return jsonify({'response': ai_msg.content})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Run the Flask app on the specified host and port
    app.run(host='0.0.0.0', port=8000)
