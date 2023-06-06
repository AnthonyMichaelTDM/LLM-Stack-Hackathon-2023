# CacheChat-v2

Chat about your data, production-grade style.

## Notes

- You don't need to upload anything to chat. It just helps the AI out, and who doesn't want to do that?
- You can upload as many files/URLs as you want at any point in the conversation.
- A list of accepted file/URL file formats can be found [here](https://textract.readthedocs.io/en/stable/#currently-supporting). Keep in mind that it sometimes won't be able to extract the text from the file (a blurry image for example).
- Once a file/URL is uploaded, it can be removed by clicking the "remove" button.

## Setup

1. Install conda if necessary:

    ```bash
    # Install conda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation
    # If on Windows, install chocolately: https://chocolatey.org/install. Then, run:
    # choco install make
    ```

2. Create the conda environment locally:

    ```bash
    git clone https://github.com/andrewhinh/serverchat.git
    cd serverchat
    conda env update --prune -f environment.yml
    conda activate serverchat
    pip install -r requirements.txt
    export PYTHONPATH=.
    echo "export PYTHONPATH=.:$PYTHONPATH" >> ~/.bashrc (or ~/.zshrc)
    # If on Windows, the last two lines probably won't work. Check out this guide for more info: https://datatofish.com/add-python-to-windows-path/
    ```

3. Using `.env.template` as reference, create a `.env` file with your [OpenAI API key](https://beta.openai.com/account/api-keys), and reactivate the conda environment:

    ```bash
    conda activate serverchat
    ```

4. Run the application using streamlit:

   ```bash
   streamlit run app.py
   ```

5. Run the Qdrant server on a separate terminal:

   ```bash
   docker run -p 6333:6333 qdrant/qdrant:latest
   ```

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
