$(document).ready(function () {
    loadChatHistory();

    const md = new markdownit();
    $("#askForm").submit(function (event) {
        event.preventDefault();
        let question = $("#questionInput").val();
        let userMessage = $('<div class="message user-message"></div>').text(question);
        $(".chat").append(userMessage);
        
        // Collect the conversation history
        let conversation = [];
        $(".chat .message").each(function() {
            let role = $(this).hasClass("user-message") ? "user" : "assistant";
            let content = $(this).text();
            if ($(this).find(".copy-button").length) {
                content = content.replace("Copy", ""); // Remove "Copy" from the copied text
            }
            conversation.push([role, content]);
        });

        // Send the conversation history along with the question
        $.post("/ask", { question: question, conversation: JSON.stringify(conversation) }, function (data) {
            // Convert the responseText from Markdown to HTML
            const formattedText = md.render(data.response);
        
            let aiMessage = $('<div class="message ai-message"></div>').html(formattedText);
            let copyButton = $('<button class="copy-button">Copy</button>');
            aiMessage.append(copyButton);
            $(".chat").append(aiMessage);
            saveChatHistory();
        });

        $("#questionInput").val(""); // Clear input after submission
    });
});

$(document).on("click", ".copy-button", function () {
    let textToCopy = $(this).parent().text().replace("Copy", ""); // Remove "Copy" from the copied text
    let tempInput = $("<input>");
    $("body").append(tempInput);
    tempInput.val(textToCopy).select();
    document.execCommand("copy");
    tempInput.remove();
});

function loadChatHistory() { 
    const chatHistory = localStorage.getItem('chatHistory');
    if (chatHistory) {
      $(".chat").html(chatHistory);
    }
}

function saveChatHistory() {
    const chatBox = $(".chat");
    localStorage.setItem('chatHistory', chatBox.html());
}

function clearChatHistory() {
    localStorage.removeItem('chatHistory');
    $(".chat .message").remove(); // Remove only messages, not the entire chat content
}
