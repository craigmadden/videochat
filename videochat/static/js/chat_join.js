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

	call_button = document.getElementById('join-call');
	call_button.addEventListener('click', function() {
		joinCall(peer,rtcid,window.localStream)
	},false);
}

function joinCall(peer,rtcid,mediastream){
	var call = peer.call(rtcid, mediastream);

	peer.on('call', function(call){
		call.answer(mediastream);
	});

	call.on('stream', function(stream){
    	$('#their-video').prop('src', URL.createObjectURL(stream));
  	});

  	$.post("/update_status/", {'uuid':rtcid, 'status':'Active','csrfmiddlewaretoken': csrftoken}, 
  		function(data) {
   			console.log(data);
	});
}

main();


