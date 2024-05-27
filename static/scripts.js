$(document).ready(function () {
  loadChatHistory();

  const md = new markdownit();
  $("#askForm").submit(function (event) {
    event.preventDefault();
    let question = $("#questionInput").val();
    let userMessage = $('<div class="message user-message"></div>').text(
      question
    );
    $(".chat").append(userMessage);

    let conversation = [];
    $(".chat .message").each(function () {
      let role = $(this).hasClass("user-message") ? "user" : "assistant";
      let content = $(this).text();
      conversation.push([role, content]);
    });

    $.post(
      "/ask",
      { question: question, conversation: JSON.stringify(conversation) },
      function (data) {
        const formattedText = md.render(data.response);
        let aiMessage = $('<div class="message ai-message"></div>').html(
          formattedText
        );
        let copyButton = $('<button class="copy-button">Copy</button>');
        aiMessage.append(copyButton);
        $(".chat").append(aiMessage);
        saveChatHistory();
      }
    ).fail(function () {
      alert("An error occurred while sending the request.");
    });

    $("#questionInput").val("");
  });
});

$(document).on("click", ".copy-button", function () {
  let textToCopy = $(this).parent().text().replace("Copy", ""); // Remove "Copy" from the copied text
  navigator.clipboard
    .writeText(textToCopy)
    .then(function () {
      console.log("Text copied to clipboard");
    })
    .catch(function (err) {
      console.error("Could not copy text: ", err);
    });
});

function loadChatHistory() {
  const chatHistory = localStorage.getItem("chatHistory");
  if (chatHistory) {
    $(".chat").html(chatHistory);
  }
}

function saveChatHistory() {
  const chatBox = $(".chat");
  localStorage.setItem("chatHistory", chatBox.html());
}

function clearChatHistory() {
  localStorage.removeItem("chatHistory");
  $(".chat .message").remove(); // Remove only messages, not the entire chat content
}
