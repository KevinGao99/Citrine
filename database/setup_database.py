import sqlite3

def setup_database():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def store_document(content):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO documents (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()

def retrieve_documents():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT content FROM documents')
    documents = cursor.fetchall()
    conn.close()
    return [doc[0] for doc in documents]

# Setup and store example documents
setup_database()
store_document("Example document content 1")
store_document("Example document content 2")
print(retrieve_documents())
