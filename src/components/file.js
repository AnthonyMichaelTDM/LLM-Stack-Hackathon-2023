import React, { Component } from 'react'

class FileUploader extends Component {
    render() {
        return (
            <div className="FileUploader">
                <label htmlFor="fileUploader">Choose file(s):</label>
                <input type="file" id="fileUploader" name="fileUploader" multiple></input>
            </div>
        )
    }
}

export default FileUploader