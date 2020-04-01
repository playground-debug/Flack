document.addEventListener('DOMContentLoaded', () => {

	// disabling the send button
	document.querySelector('#send').disabled = true;

			// enabling create button only if their is text in input field
			document.querySelector('#comment').onkeyup = () => {
				if (document.querySelector('#comment').value.length > 0) {
					document.querySelector('#send').disabled = false;
				}
				else
					document.querySelector('#send').disabled = true;
			};

	// connect to websocket
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

	// when connected configure buttons
	socket.on('connect', () => {

		socket.emit('joined');

		document.querySelector('#leave').onclick = () => {
			socket.emit('leaved');
			window.location.replace('/main');
		}

		document.querySelector('#send').onclick = () => {
			const comment = document.querySelector('#comment').value;
			socket.emit('comment', {'comment': comment});
		}

	});

	socket.on('status', data => {

        // Broadcast message of joined user.
        let row = `${data.msg}`
        document.querySelector('#chat').value += row + '\n';
    })


	socket.on('status_leave', data => {

        // Broadcast message of leaved user.
        let row = `${data.msg}`
        document.querySelector('#chat').value += row + '\n';
    })

	socket.on('message', data => {

        // Broadcast send message.
        let row = `${data.username}:  ${data.comment}   (${data.interval})`
        document.querySelector('#chat').value += row + '\n';
        document.querySelector('#comment').value = '';
        document.querySelector('#send').disabled = true;
    })
});