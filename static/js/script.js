async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput) return;
    
    displayMessage(userInput, 'user');
    document.getElementById('user-input').value = '';
    
    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userInput })
    });
    
    const data = await response.json();
    displayMessage(data.response, 'bot');
}

function displayMessage(message, sender) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = message;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
