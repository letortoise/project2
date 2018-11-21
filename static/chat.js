document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configue input group
    socket.on('connect', () => {

        const messageInput = document.querySelector('#message');
        console.log("hello")

        // Submitting the input or selecting the button should emit the "send message" event
        document.querySelector('#form').onsubmit = () => {
            const message = messageInput.value;
            messageInput.value = '';
            socket.emit('send message', {'message': message});

            //Don't allow the page to reload
            return false;
        };
    });

    // When a new message is announced, update the page
    socket.on('new message', data => {

        // Create message element
        const h = document.createElement('h5');
        h.innerHTML = `${data.message}`;
        document.querySelector('#chat-window').append(h);

    });
});
