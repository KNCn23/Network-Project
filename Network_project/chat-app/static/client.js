function startChat(username) {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    document.getElementById('send-button').onclick = () => {
        const messageInput = document.getElementById('message-input');
        const message = messageInput.value;
        if (message.trim()) {
            socket.send({ 'username': username, 'message': message });
            messageInput.value = '';
        }
    };

    socket.on('message', (msg) => {
        const messageContainer = document.getElementById('message-container');
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');  // Mesajları kart formatında göster
        messageElement.textContent = msg;
        messageContainer.appendChild(messageElement);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    });
}
