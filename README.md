# LLM Stack Hackathon 2023

## Setup

1. Install conda if necessary:

    ```bash
    # Install conda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation
    # If on Windows, install chocolately: https://chocolatey.org/install. Then, run:
    # choco install make
    ```

2. Create the conda environment locally:

    ```bash
    git clone https://github.com/AnthonyMichaelTDM/ LLM-Stack-Hackathon-2023.git
    cd LLM-Stack-Hackathon-2023
    conda env update --prune -f environment.yml
    conda activate llm
    pip install -r requirements.txt
    export PYTHONPATH=.
    echo "export PYTHONPATH=.:$PYTHONPATH" >> ~/.bashrc (or ~/.zshrc)
    # If on Windows, the last two lines probably won't work. Check out this guide for more info: https://datatofish.com/add-python-to-windows-path/
    ```

3. Sign up for an OpenAI account and get an API key [here](https://beta.openai.com/account/api-keys).
4. Populate a `.env` file with your key in the format of `.env.template`, and reactivate the environment.

## Save Requirements

- `pip freeze > requirements.txt`

## Run Qdrant Instance

- `docker run -p 6333:6333 qdrant/qdrant:latest`

## Tech Stack

- OpenAI api - llm
- Qdrant - vector database
- react
- pandas
- ...


## Run gradio
```
gradio frontend/langchain_gradio.py
```
