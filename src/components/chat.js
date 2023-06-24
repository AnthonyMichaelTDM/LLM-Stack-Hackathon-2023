import React, { Component } from 'react'

class ChatBox extends Component {
    render() {
        return (
            <div className="ChatBox">
                <form novalidate className="chat-form">
                    <label htmlFor="chat"></label>
                    <input type="text" id="chat" name="chat" required></input>
                    <p class="error" aria-live="polite"></p>
                    <button class="send-button">Hmm</button>
                </form>
            </div>
        )
    }

    chatForm = document.querySelector(".chat-form");
    chatText = document.querySelector("#chat");
    chatTextError = document.querySelector("#chat + p.error");
    hmmButton = document.querySelector(".send-button");

    // Call /token endpoint with username and password
    // Call /chat endpoint with conversation_id and message
}

export default ChatBox