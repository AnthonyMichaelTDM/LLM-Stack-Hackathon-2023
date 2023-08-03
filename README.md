# Project

## Contributing

To contribute, check out the [guide](./CONTRIBUTING.md).

### Frontend (Node.js + React + Vercel)

Move into the `frontend` directory:

   ```bash
   cd frontend
   ```

Create a `.env` file:

   ```bash
   JWT_SECRET=$(openssl rand -hex 32)
   echo "JWT_SECRET=$JWT_SECRET" >> .env
   ```

Install the npm dependencies:

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

To deploy the build to Vercel:

   ```bash
   npm i -g vercel
   vercel
      # Set up and deploy “path to your project”? [Y/n] y
      # Which scope do you want to deploy to? <org account>
      # Link to existing project? [y/N] n
      # What’s your project’s name? <project name>
      # In which directory is your code located? ./
      # Want to override the settings? [y/N] n
   ```

### Backend (Conda + FastAPI + Deta Space)

Move into the `backend` directory:

   ```bash
   cd backend
   ```

Create a `.env` file:

   ```bash
   # Get an OpenAI API key [here](https://platform.openai.com/signup)
   OPENAI_API_KEY=<your key here>
   echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> .env
   ```

Create the conda environment locally:

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
   gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0
   ```

To deploy the backend to Deta Space:

- Follow steps from [creating a new project in Space](https://fastapi.tiangolo.com/deployment/deta/#create-a-new-project-in-space) to [deploying it to Space](https://fastapi.tiangolo.com/deployment/deta/#check-it).

   ```bash
   space new
   space push
   ```
