# Project

## Contributing

To contribute, check out the [guide](./CONTRIBUTING.md).

### Frontend (Node.js + React + Vite + Vercel)

Set up your local environment:

   ```bash
   make frontend-setup
      # cd frontend
      # JWT_SECRET=$(openssl rand -hex 32)
      # echo "JWT_SECRET=$JWT_SECRET" >> .env
      # npm install
      # npm i -g vercel
   ```

To lint the code:

   ```bash
   npm run lint
   ```

To run the frontend locally:

   ```bash
   npm run dev
   ```

To create a production build locally:

   ```bash
   npm run build
   ```

To preview the production build locally:

   ```bash
   npm run preview
   ```

If a build needs to be deployed to Vercel manually (pushing to GitHub will automatically deploy to Vercel):

   ```bash
   cd ..
   vercel deploy
      # Set up and deploy “path to your project”? [Y/n] y
      # Which scope do you want to deploy to? <org account>
      # Link to existing project? [y/N] n
      # What’s your project’s name? <project name>
      # In which directory is your code located? ./frontend
      # Want to override the settings? [y/N] n
   ```

### Backend (Conda + FastAPI + Deta Space)

Either create the conda environment locally:

   ```bash
   make conda-update
   conda activate project
      # conda env update --prune -f environment.yml
   ```

Or create the conda environment in a Docker container:

- In [this guide](https://code.visualstudio.com/docs/devcontainers/containers#_getting-started):
  - [Install the prerequisites](https://code.visualstudio.com/docs/devcontainers/containers#_getting-started).
  - Then open the current working directory (`backend`) [in the container](https://code.visualstudio.com/docs/devcontainers/containers#_quick-start-open-an-existing-folder-in-a-container).

Set up the conda environment:

   ```bash
   make pip-tools
   make backend-setup
      # make pip-tools
         # pip install pip-tools==7.1.0 setuptools==68.0.0
         # pip-compile requirements/prod.in && pip-compile requirements/dev.in
         # pip-sync requirements/prod.txt requirements/dev.txt
      # make backend-setup
         # pre-commit install
         # export PYTHONPATH=.
         # echo "export PYTHONPATH=.:$PYTHONPATH" >> ~/.bashrc
         # cd backend
   ```

Create a `.env` file:

   ```bash
   # Get an OpenAI API key [here](https://platform.openai.com/signup)
   OPENAI_API_KEY=<your key here>
   echo "OPENAI_API_KEY=$OPENAI_API_KEY" >> .env
   ```

To bump transitive dependencies:

   ```bash
   make pip-tools-upgrade
   ```

To lint the code manually:

   ```bash
   pre-commit run --all-files
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
