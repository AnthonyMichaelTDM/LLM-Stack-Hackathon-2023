# Backend API

A backend api for the website that implements a /chat endpoint.

## Contributing

To contribute, check out the [guide](../CONTRIBUTING.md).

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/andrewhinh/cachechat.git
   cd cachechat
   ```

2. Using `.env.template` as reference, create a `.env` file that has:
   a. [OpenAI API key](https://beta.openai.com/account/api-keys)
   b. JWT secret key (created by running `openssl rand -hex 32`)

3. Install conda if necessary:

   ```bash
   # Install conda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation
   # If on Windows, install chocolately: https://chocolatey.org/install. Then, run:
   # choco install make
   ```

4. Create the conda environment locally:

   ```bash
   cd backend
   make conda-update
   conda activate cachechat
   make pip-tools
   pre-commit install
   export PYTHONPATH=.
   echo "export PYTHONPATH=.:$PYTHONPATH" >> ~/.bashrc (or ~/.zshrc)
   # If on Windows, the last two lines probably won't work. Check out this guide for more info: https://datatofish.com/add-python-to-windows-path/
   ```

5. Run the server on a separate terminal:

   ```bash
   gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0
   ```

### Development

To lint every file (after staging changes with `git add`, though this is run automatically when you try to commit):

```bash
pre-commit run
```

To test every file:

```bash
pytest
```
