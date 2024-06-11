const socket = new WebSocket("ws://localhost:8000/ws/chat/")

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  const message = data["message"];
  document.querySelector("#message-list").lastChild.innerHTML = message;
};

document.forms.input.onsubmit = function (event) {
  event.preventDefault()

  const message = this.message.value
  socket.send(JSON.stringify({
    "message": message
  }));

  document.querySelector("#message-list").appendChild(document.createElement("div"))
  document.querySelector("#message-list").lastChild.innerText = message;
  document.querySelector("#message-list").appendChild(document.createElement("div"))
}
