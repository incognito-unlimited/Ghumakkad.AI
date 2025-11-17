document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("message-input");
    const chatWindow = document.getElementById("chat-window");

    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault(); // Stop form from reloading page

        const message = messageInput.value.trim();
        if (!message) return;

        // 1. Display user's message as plain text (safe)
        addMessageToChat(message, "user");
        messageInput.value = ""; // Clear input

        // 2. Show a loading indicator
        const loadingEl = addMessageToChat("Typing...", "loading");

        try {
            // 3. Send message to Flask backend
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: message }),
            });

            // 4. Remove loading indicator
            chatWindow.removeChild(loadingEl);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // 5. Display AI's response (will be parsed as HTML)
            if (data.response) {
                addMessageToChat(data.response, "ai");
            } else if (data.error) {
                addMessageToChat(`Error: ${data.error}`, "ai");
            }

        } catch (error) {
            // Remove loading and show error
            chatWindow.removeChild(loadingEl);
            console.error("Fetch error:", error);
            addMessageToChat("Sorry, I couldn't connect to the server. Please try again.", "ai");
        }
    });

    // --- THIS FUNCTION IS MODIFIED ---
    function addMessageToChat(text, sender) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("chat-message", sender);

        if (sender === "ai") {
            // Use marked.parse() to convert Markdown to HTML
            // This renders tables, headings, lists, etc.
            messageElement.innerHTML = marked.parse(text);
        } else {
            // For user/loading messages, we still use textContent
            // This is a security best-practice
            const p = document.createElement("p");
            p.textContent = text;
            messageElement.appendChild(p);
        }
        
        chatWindow.appendChild(messageElement);

        // Scroll to the bottom
        chatWindow.scrollTop = chatWindow.scrollHeight;
        
        return messageElement;
    }
});