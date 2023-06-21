# CacheChat

Chat about your data, production-grade style.

## Notes

- You don't need to upload anything to chat. It just helps the AI out, and who doesn't want to do that?
- You can upload data at any point in the conversation.
- Once data is uploaded, it can be removed by clicking the "remove" button.

## Contributing

To contribute, check out the [guide](./CONTRIBUTING.md).

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/andrewhinh/cachechat.git
   cd cachechat
   ```

2. Using `.env.template` as reference, create a `.env` file with the following:
   - [OpenAI API key](https://beta.openai.com/account/api-keys)
   - JWT secret key (created by running `openssl rand -hex 32`)

3. Install conda if necessary:

   ```bash
   # Install conda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation
   # If on Windows, install chocolately: https://chocolatey.org/install. Then, run:
   # choco install make
   ```

4. Create the conda environment locally:

   ```bash
   make conda-update
   conda activate cachechat
   make pip-tools
   export PYTHONPATH=.
   echo "export PYTHONPATH=.:$PYTHONPATH" >> ~/.bashrc (or ~/.zshrc)
   # If on Windows, the last two lines probably won't work. Check out this guide for more info: https://datatofish.com/add-python-to-windows-path/
   ```

### Development

(Recommended) To make `pre-commit` run automatically before every commit:

```bash
pre-commit install
```

To test the backend:

```bash
pytest
```

To run the backend locally:

   ```bash
   gunicorn backend.app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0
   ```
