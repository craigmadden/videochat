/* Main WebRTC code 
*  Requests access to camera and microphone
*  Creates a video stream
*/


function main() {
  // Get the chat ID from the URL
  //sessid = sessionStorage.getItem('chatid');
  rtcid = window.location.href.split('/').pop();
  /*
  if(sessid != rtcid) {
    sessionStorage.setItem('chatid',rtcid);
    console.log("SessionID: " + sessid)
  } else {
    console.log("Equal")
    window.location="/";
  }
  */


  // Compatibility shim
  navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

  if(navigator.getUserMedia) {
    navigator.getUserMedia({audio: true, video: true}, function(stream){
        // Set your video displays
        $('#chatinfo').show()
        $('#chatinstructions').hide()
        $('#chatvideo').show()
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
      // Show the "chatcontrol" div that contains the end-call button
      $('#chatcontrol').show();
      $('#chatinfo').hide();
    });
  });

  peer.on('error', function(err){
    alert(err.message);
    // Return to step 2 if error occurs
    // update some UI items
  });

  end_call_button = document.getElementById('end-call');
  end_call_button.addEventListener('click', function() {
    endCall(peer)
  }, false);

  // Event listener for send email invite button
  send_button = document.getElementById('send_call');
  // When button is clicked, get value from contact drop-down menu
  send_button.addEventListener('click', function() {
    sendEmail(contact)
  }, false);
}

function endCall(peer){
  peer.destroy(true);
  window.location.href = "/";
}

function sendEmail(contact){
  // AJAX funtion call here

}
main();