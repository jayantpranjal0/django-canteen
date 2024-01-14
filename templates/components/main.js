import WebSocket from 'ws';
// open the websocket connection
try {
    alert("Connecting to server...");
    const chatSocket = new WebSocket("ws://" + window.location.host + "/customer");
    chatSocket.onopen = function() {
        console.log("Socket opened.");
        alert("Connection Established!!");
    }

    chatSocket.onclose = function() {
        console.log("Socket closed.");
        alert("Connection Closed!! Please refresh the page.");
    }
} catch(err) {
    console.log(err);
    alert("Error: " + err);
    alert("Please refresh the page.");
}