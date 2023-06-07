import React, { Component } from 'react'

class UrlUploader extends Component {
    render() {
        return (
            <div className="UrlUploader">
                <label htmlFor="urlUploader">Enter a URL:</label>
                <input type="text" id="urlUploader" name="urlUploader"></input>
                <button>Add URL</button>
            </div>
        )
    }
}

export default UrlUploader