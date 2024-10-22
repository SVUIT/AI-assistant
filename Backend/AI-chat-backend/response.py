from flask import Flask, request, jsonify
from langchain_core.messages import HumanMessage
from create_chain import rag_chain,retriever

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
        count = 0
        score = 0
        relevant_docs = ""
        scene = {
    "Xin chào": "Chào bạn, tôi là chatbot hỗ trợ của SVUIT. Tôi có thể giúp gì cho bạn?"
    }
        if question in scene:
            return jsonify({'response': scene[question],'source':""})
        else:
            # Tính score
            relevant_results=retriever.invoke(question)
            for x in range(len(relevant_results)):
                score+=float(relevant_results[x].metadata.get('score'))
            score /=len(relevant_results)
            if ( score < 0.4):
                return jsonify({'response': "Tôi xin lỗi, tôi không có đủ thông tin để trả lời câu hỏi này",'source':""})
            else:
                for x in range(len(relevant_results)):
                    if (relevant_docs.__contains__(relevant_results[x].metadata.get('source')) | relevant_results[x].metadata.get('source').__contains__("docs")):
                        continue
                    relevant_docs +=(relevant_results[x].metadata.get('source'))
                    count+=1
                    if count==2:
                        break
                    relevant_docs+='|'
                ai_msg = rag_chain.invoke({"question": question, "chat_history": chat_history , "topic": "UIT, internet and information technology"})
                            
                # Update chat history with the new messages
                chat_history.extend([HumanMessage(content=question), ai_msg])
                return jsonify({'response': ai_msg.content,'source': relevant_docs})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    # Run the Flask app on the specified host and port
    app.run(host='0.0.0.0', port=8000)