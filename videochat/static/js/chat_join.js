/* Main WebRTC code 
*  Requests access to camera and microphone
*  Creates a video stream
*/

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

function joinCall(){
	var call = peer.call(rtcid, window.localStream);

	peer.on('call', function(call){
		call.answer(window.localStream);
	});

	call.on('stream', function(stream){
    	$('#their-video').prop('src', URL.createObjectURL(stream));
  });
}


// PeerJS object with auto generated ID
var peer = new Peer({ key: 'lwjd5qra8257b9', debug: 3, config: {'iceServers': [
  { url: 'stun:stun.l.google.com:19302' } // Pass in optional STUN and TURN server for maximum network compatibility
]}});

$.post("/update_status/", {'uuid':rtcid, 'status':'Active','csrfmiddlewaretoken': csrftoken}, function(data) {
   console.log(data);
});

call_button = document.getElementById('join-call');
call_button.addEventListener(
	'click',
	joinCall,
	false
);



