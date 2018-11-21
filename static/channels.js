document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, allow users to create new channels
    socket.on('connect', () => {
        document.querySelector('#form').onsubmit = () => {

            // Get name for new channel and let the server know
            const name = document.querySelector('#name').value;
            socket.emit('create channel', {'name': name});
            return false;
        };
    });

    socket.on('channel created', (data) => {
        console.log(data)
        if (!data.success) {
            alert('Something went wrong');
        }

        // Update the DOM
        // const a = document.createElement('a');
        // a.classList.add('list-group-item', 'list-group-item-action');
        // document.querySelector('#channels').append(a);
    });

    document.querySelector('#add').onclick = () => {

        // Create a form where the user can create a new channel
        const a = document.createElement('a');
        a.classList.add('list-group-item', 'list-group-item-action');
        document.querySelector('#channels').append(a);

        // Let user enter a new channel name
        const input = document.createElement('input');
        a.append(input);
        document.querySelector('s');

    };



});
