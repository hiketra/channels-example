
$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);

    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var chat = $("#chat")
        var ele = $('<tr></tr>')

        var table ="<td class='handle' width='3%'><b> " + data.handle + " </b></td>" +
            "<td class='message' width='60%'>" +  data.message + "</td>" +
              "<td class='timestamp' width='10%'>" +  data.timestamp + " <br/>" +
              "<span id=" + "msgId" + $(data.id) + "'><b># " + data.id + "</b></span></td>"



        console.log(data)
        console.log(message)


        console.log(data.id + "is the ID")

        ele.append(table)


        chat.append(ele)
    };

    $("#chatform").on("submit", function(event) {
        var parentId = (document.getElementById("parentId").value == "") ? null : document.getElementById("parentId").value
        console.log("the parentId selected:" + parentId)
        var message = {
            handle: $('#handle').val(),
            message: $('#message').val(),
            first_child: null,
            parent: parentId
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });
});