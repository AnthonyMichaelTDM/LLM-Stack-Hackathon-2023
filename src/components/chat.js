import React, { Component } from 'react'

class ChatBox extends Component {
    render() {
        return (
            <div className="ChatBox">
                <label htmlFor="chatBox">Enter your input:</label>
                <input type="text" id="chatBox" name="chatBox"></input>
                <button>Send</button>
            </div>
        )
    }
}

export default ChatBox