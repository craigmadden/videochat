/* Main WebRTC code 
*  Requests access to camera and microphone
*  Creates a video stream
*/

function main() {
	rtcid = window.location.href.split('/').pop();

	// Compatibility shim
	navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

	if(navigator.getUserMedia) {
		navigator.getUserMedia({audio: true, video: true}, function(stream){
		    // Set your video displays
		    $('#chatinfo').show();
		    $('#chatinstructions').hide();
        	$('#chatvideo').show();
		    $('#my-video').prop('src', URL.createObjectURL(stream));

		    window.localStream = stream;
		}, function(err) { 
			console.log("The following error occured: " + err.name);
		});
	} else {
		console.log("getUserMedia not supported");
	}

	// PeerJS object with auto generated ID
	var peer = new Peer({ key: 'lwjd5qra8257b9', debug: 3, config: {'iceServers': [
	  { url: 'stun:stun.l.google.com:19302' } // Pass in optional STUN and TURN server for maximum network compatibility
	]}});

	peer.on('close', function() {
		console.log("The connection has been closed.")
	});

	call_button = document.getElementById('join-call');
	call_button.addEventListener('click', function() {
		joinCall(peer,rtcid,window.localStream)
	},false);

	end_call_button = document.getElementById('end-call');
	end_call_button.addEventListener('click', function() {
		endCall(peer)
	}, false);
}

function joinCall(peer,rtcid,mediastream){
	var call = peer.call(rtcid, mediastream);

	//$('#join-call').hide()

	peer.on('call', function(call){
		call.answer(mediastream);
	});

	call.on('stream', function(stream){
    	$('#their-video').prop('src', URL.createObjectURL(stream));
    	// Show the "chatcontrol" div that contains the end-call button
    	$('#chatcontrol').show();
    	// Hide the Join button once the connection is established
    	$('#chatinfo').hide();

  	});

  	$.post("/update_status/", {'uuid':rtcid, 'status':'Active','csrfmiddlewaretoken': csrftoken}, 
  		function(data) {
   			console.log(data);
	});
}

function endCall(peer){
	peer.destroy(true)
	window.location.href = "/";
}

main();