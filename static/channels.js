document.addEventListener('DOMContentLoaded', () => {

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

    document.querySelector('#form').onsubmit = () => {

        // Initialize new request
        const request = new XMLHttpRequest();
        const name = document.querySelector('#name').value;
        request.open('POST', '/create_channel');

        // Callback for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);

            if (data.success) {
                alert('channel was added');
            }
            else {
                alert('something failed');
            }

        };

        // Add data to send with request
        const data = new FormData();
        data.append('name', name);

        // Send request
        request.send(data);
        return false;
    };

});
