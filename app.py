from flask import Flask, request, jsonify
from chatbot import ChatDoc

app = Flask(__name__)
chat_doc = ChatDoc()

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.json.get('query')
    if not user_query:
        return jsonify({'error': 'No query provided'}), 400

    response = chat_doc.process_query(user_query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
