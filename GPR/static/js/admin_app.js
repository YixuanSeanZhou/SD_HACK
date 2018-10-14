var socket;

var status_response;

function pause() {
  console.log("Pause");
  socket.emit("admin_pause");
}

function status_update() {
  console.log("Sending status request");
  return socket.emit("status_request");
}

$(document).ready(function() { 
  socket = io.connect("http://" + document.domain + ":" + location.port);

  socket.on("status_update", function(msg) {
    $("#status").html(msg.playing ? "Live" : "Offline");
  });

  socket.on("chunk", function(msg) {
    console.log(msg)
  });

  $("#pause").click(pause);

  $("#status_update").click(status_update);

  status_update();
});

