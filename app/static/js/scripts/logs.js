// Socketio
$(document).ready(function(e){
	if(document.location.pathname=="/panel/logs/"){
		var socket = io.connect("/logServer");
		socket.emit("startLogsSabu");
		socket.on("receiveLogsSabu",function(data){
			$("#setLogs").html(data.replace(/\n/g, "<br />"));
			$("#masterSetLogs").animate({ scrollTop: $("#masterSetLogs")[0].scrollHeight }, 1000);
		})
	}
});