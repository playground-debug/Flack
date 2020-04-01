document.addEventListener('DOMContentLoaded', () => {


	// disabling the create button
	document.querySelector('#create').disabled = true;

			// enabling create button only if their is text in input field
			document.querySelector('#channel_name').onkeyup = () => {
				if (document.querySelector('#channel_name').value.length > 0) {
					document.querySelector('#create').disabled = false;
				}
				else
					document.querySelector('#create').disabled = true;
			};

	// connect to websocket
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

	// when connected configure buttons
	socket.on('connect', () => {

		// create button will emit create channel request to server
		document.querySelector('#create').onclick = () => {
			const channel_name = document.querySelector('#channel_name').value;
			socket.emit('create channel', {'channel_name': channel_name});
		};

	});

	// when a new vote is announced add it to unordered list
	socket.on('announce channel', data => {
		check = parseInt(data.yes);
		if(check){
			const li = document.createElement('li')
			const a = document.createElement('a')
			a.innerHTML = `${data.channel_name}`;
			a.href = `channel/${data.channel_name}`;
			li.append(a);
			document.querySelector('#channel_list').append(li);
			document.querySelector('#channel_name').value = '';
		}
		else {
			document.querySelector('#channel_name').value = '';
			window.alert(data.message)
			document.querySelector('#create').disabled = true;
		}


	});

});