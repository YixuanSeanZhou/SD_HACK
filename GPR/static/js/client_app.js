var socket;

$(document).ready(function() {
  socket = io.connect("http://" + document.domain + ":" + location.port);

  socket.on("connect", function() {
    console.log("Connected");
  });

  socket.on("disconnect", function() {
    console.log("Disconnected");
  });

  socket.on("chunk", function(msg) {
    console.log("Chunk recieved");
    //$("#log").append("<p>"+msg.msg+"</p>");
  });
});
