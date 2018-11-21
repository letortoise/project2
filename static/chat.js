document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configue input group
    socket.on('connect', () => {

        const messageInput = document.querySelector('#message');

        // Submitting the input or selecting the button should emit the "send message" event
        const sendMessage = () => {
            const message = messageInput.value;
            messageInput.value = '';
            socket.emit('send message', {'message': message});
        };
        document.querySelector('#send').onclick = sendMessage;
        document.querySelector('#message').onkeypress = function(event) {
            // Send the message if the user hit enter
            if (event.key == 'Enter')
                sendMessage();
        };
    });

    // When a new message is announced, update the page
    socket.on('new message', data => {

        // Create new message
        const h = document.createElement('h5');
        h.innerHTML = `${data.username}: ${data.message}`;
        document.querySelector('#chat-window').append(h);

    });
});
