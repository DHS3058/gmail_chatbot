(function () {
    // Create chat icon and chatbox
    const chatIcon = document.createElement("div");
    chatIcon.innerHTML = "💬";
    chatIcon.style.position = "fixed";
    chatIcon.style.bottom = "20px";
    chatIcon.style.right = "20px";
    chatIcon.style.fontSize = "24px";
    chatIcon.style.cursor = "pointer";
    chatIcon.style.zIndex = "1000";
    chatIcon.style.backgroundColor = "white";
    chatIcon.style.borderRadius = "50%";
    chatIcon.style.width = "40px";
    chatIcon.style.height = "40px";
    chatIcon.style.display = "flex";
    chatIcon.style.alignItems = "center";
    chatIcon.style.justifyContent = "center";
    chatIcon.style.boxShadow = "0 2px 10px rgba(0,0,0,0.2)";
    
    const chatbox = document.createElement("div");
    chatbox.style.position = "fixed";
    chatbox.style.bottom = "70px";
    chatbox.style.right = "20px";
    chatbox.style.width = "350px";
    chatbox.style.height = "500px";
    chatbox.style.backgroundColor = "white";
    chatbox.style.borderRadius = "10px";
    chatbox.style.boxShadow = "0 2px 10px rgba(0,0,0,0.2)";
    chatbox.style.display = "none";
    chatbox.style.flexDirection = "column";
    chatbox.style.zIndex = "1000";
    
    chatbox.innerHTML = `
        <div style="padding: 15px; border-bottom: 1px solid #eee; font-weight: bold;">
            AI Chat Assistant
        </div>
        <div id="chat-messages" style="flex: 1; padding: 15px; overflow-y: auto;"></div>
        <div style="padding: 15px; border-top: 1px solid #eee; display: flex; gap: 8px;">
            <input type="text" id="chat-input" style="flex: 1; padding: 8px; border: 1px solid #ddd; border-radius: 4px;" placeholder="Type your message...">
            <button id="use-selected-text" style="padding: 8px 12px; background: #4285f4; color: white; border: none; border-radius: 4px; cursor: pointer;">Use Selected Text</button>
        </div>
    `;

    
    document.body.appendChild(chatIcon);
    document.body.appendChild(chatbox);
    
    // Toggle chatbox visibility
    chatIcon.addEventListener("click", () => {
        chatbox.style.display = chatbox.style.display === "none" ? "flex" : "none";
    });
    
    // Handle message sending
    const chatInput = chatbox.querySelector("#chat-input");
    const useSelectedTextBtn = chatbox.querySelector("#use-selected-text");
    
    // Handle text input
    chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter" && chatInput.value.trim()) {
            const message = chatInput.value.trim();
            chatInput.value = "";
            addMessageToChat("user", message);
            sendChatMessage(message);
        }
    });
    
    // Handle selected text
    useSelectedTextBtn.addEventListener("click", () => {
        const selection = window.getSelection().toString().trim();
        if (selection) {
            addMessageToChat("user", "Selected text: " + selection);
            sendChatMessage(selection, true);
        } else {
            addMessageToChat("system", "No text selected. Please select some text first.");
        }
    });

    // // Maintain conversation history
    let conversationHistory = [];

    function addMessageToChat(sender, message) {
        const messagesDiv = chatbox.querySelector("#chat-messages");
        const messageDiv = document.createElement("div");
        messageDiv.style.marginBottom = "10px";
        messageDiv.style.padding = "8px 12px";
        messageDiv.style.borderRadius = "8px";
        messageDiv.style.backgroundColor = sender === "user" ? "#e3f2fd" : "#f5f5f5";
        messageDiv.style.alignSelf = sender === "user" ? "flex-end" : "flex-start";
        messageDiv.style.maxWidth = "80%";
        messageDiv.textContent = message;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        // Store conversation history
        conversationHistory.push({ sender, message });
    }


    
    // function addMessageToChat(sender, message) {
    //     const messagesDiv = chatbox.querySelector("#chat-messages");
    //     const messageDiv = document.createElement("div");
    //     messageDiv.style.marginBottom = "10px";
    //     messageDiv.style.padding = "8px 12px";
    //     messageDiv.style.borderRadius = "8px";
    //     messageDiv.style.backgroundColor = sender === "user" ? "#e3f2fd" : "#f5f5f5";
    //     messageDiv.style.alignSelf = sender === "user" ? "flex-end" : "flex-start";
    //     messageDiv.style.maxWidth = "80%";
    //     messageDiv.textContent = message;
    //     messagesDiv.appendChild(messageDiv);
    //     messagesDiv.scrollTop = messagesDiv.scrollHeight;
    // }
    
    function sendChatMessage(message, isSelectedText = false) {
        fetch("http://localhost:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                message,
                isSelectedText 
            })

        })
        .then(response => response.json())
        .then(data => {
            addMessageToChat("ai", data.response);
        })
        .catch(error => {
            addMessageToChat("ai", "Sorry, I'm having trouble responding right now.");
            console.error("Chat error:", error);
        });
    }

    function extractOpenedEmail() {

        let emailData = {};

        // Get sender
        let senderElement = document.querySelector(".gD") || document.querySelector("h3 span[email]");
        emailData.email_sender = senderElement ? senderElement.innerText : "Unknown";

        // Get subject
        let subjectElement = document.querySelector("h2");
        emailData.email_subject = subjectElement ? subjectElement.innerText : "No Subject";

        // Get email body
        let bodyElement = document.querySelector(".a3s.aXjCH");
        emailData.email_content = bodyElement ? bodyElement.innerText : "No Content";

        return emailData;
    }

    function sendEmailDataToBackend() {
        let emailData = extractOpenedEmail();

        fetch("http://localhost:5000/fetch-opened-email", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(emailData)

        })
        .then(response => response.json())
        .then(data => {
            displayAIResponse(data.response);
        })
        .catch(error => {
            console.error("Error fetching AI response:", error);
            displayAIResponse("Sorry, I'm having trouble processing this email.");
        });

    }

    function displayAIResponse(responseText) {
        addMessageToChat("ai", responseText);
    }


    function checkEmailOpen() {
        let emailContent = extractOpenedEmail().email_content;
        if (emailContent && emailContent.length > 10) {
            sendEmailDataToBackend();
        }
    }

    setInterval(checkEmailOpen, 5000);
})();
