/* Main WebRTC code 
*  Requests access to camera and microphone
*  Creates a video stream
*/


function main() {
  // Get the chat ID from the URL
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

  // PeerJS object
  var peer = new Peer(rtcid,{ key: 'lwjd5qra8257b9', debug: 3, config: {'iceServers': [
    { url: 'stun:stun.l.google.com:19302' } // Pass in optional STUN and TURN server for maximum network compatibility
  ]}});

  // Update database with Waiting status
  var data = {'uuid':rtcid, 'status':'Waiting','csrfmiddlewaretoken': csrftoken};
  var args = {type:"POST", dataType:'json', url:"/update_status/",data:data};
  $.post("/update_status/", data, function(data) {
     console.log(data);
  });


  peer.on('open', function(){
    $('#my-id').text(peer.id);
  });

  // Receiving a call
  peer.on('call', function(call){
    // Answer the call automatically (instead of prompting user) for demo purposes
    call.answer(window.localStream);
    // Wait for stream on the call, then set peer video display
    call.on('stream', function(stream){
      $('#their-video').prop('src', URL.createObjectURL(stream));
    });
  });

  peer.on('error', function(err){
    alert(err.message);
    // Return to step 2 if error occurs
    // update some UI items
  });
}

main();