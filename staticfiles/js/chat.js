const socket = new WebSocket("ws://localhost:8000/ws/chat/")

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  const id = data["id"];
  if (!document.getElementById(id)) {
    div = document.createElement("div");
    div.setAttribute("id", id)
    div.classList.add("message");
    document.querySelector("#message-list").appendChild(div)
  }
  const content = data["content"];
  document.querySelector("#message-list").lastChild.innerHTML = content;
};

document.forms.input.onsubmit = function (event) {
  event.preventDefault()

  const message = this.message.value
  socket.send(JSON.stringify({
    "message": message
  }));
}
