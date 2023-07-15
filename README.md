# Project

## Contributing

To contribute, check out the [guide](./CONTRIBUTING.md).

Using `.env.template` as reference, create a `.env` file with the following:

- JWT secret key (created by running `openssl rand -hex 32`)

### Frontend

First, install the npm dependencies:

   ```bash
   npm install
   ```

To run all tests:

   ```bash
   npm test
   ```

To run the frontend locally:

   ```bash
   npm start
   ```

To create a production build locally:

   ```bash
   npm run build
   ```

To deploy the build to GitHub Pages:

   ```bash
   npm run deploy
   ```

### Backend

First, create the conda environment locally:

   ```bash
   make conda-update
   conda activate project
   make pip-tools
   pre-commit install
   export PYTHONPATH=.
   echo "export PYTHONPATH=.:$PYTHONPATH" >> ~/.bashrc (or ~/.zshrc)
   # If on Windows, the last two lines probably won't work. Check out this guide for more info: https://datatofish.com/add-python-to-windows-path/
   ```

To lint the code manually:

   ```bash
   pre-commit run
   ```

To run all tests:

   ```bash
   pytest
   ```

To run the backend locally:

   ```bash
   gunicorn backend.app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0
   ```

To deploy the backend to Heroku:

   ```bash
   git push heroku main
   ```
