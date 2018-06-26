const socket = io();
//socket.emit('message','nice');
socket.on('message', function (msj) {
	$('#message').append('<p class="card-text">'+msj+'</p>')
})

$(document).ready(function() {
	$('#send').on('click', function () {
		socket.send($('#myMessage').val());
		$('#myMessage').val('');
	});
});
