"""API endpoints for the chatbot.""" ""
import os

from fastapi import APIRouter, HTTPException, UploadFile
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

OPENAI_MODEL = "gpt-3.5-turbo"
router = APIRouter()


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile) -> dict[str, str]:
    """Upload a file to the vector DB.

    Parameters
    ----------
    file : UploadFile
        File to upload

    Returns
    -------
    dict[str, str]
        Filename
    """
    return {"filename": file.filename}


@router.post("/chat")
async def chat(messages: list) -> dict[str, str]:
    """Chat with the AI.

    Parameters
    ----------
    messages : list
        List of messages

    Returns
    -------
    dict[str, str]
        Answer

    Raises
    ------
    HTTPException
        If messages are missing or invalid or if OpenAI fails
    """
    try:
        if type(messages) != list or len(messages) == 0:
            raise Exception
    except Exception:
        raise HTTPException(status_code=400, detail="Missing/invalid messages")

    try:
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    "The following is a friendly conversation between a human and an AI. The AI is talkative and "
                    "provides lots of specific details from its context. If the AI does not know the answer to a "
                    "question, it truthfully says it does not know."
                ),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )

        llm = ChatOpenAI(model=OPENAI_MODEL, openai_api_key=os.getenv("OPENAI_API_KEY"))
        memory = ConversationBufferMemory(return_messages=True)
        conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

        response = conversation.predict(input=messages[-1])
        if not response:
            raise Exception
        return {"answer": response}
    except Exception:
        raise HTTPException(status_code=400, detail="OpenAI failure")
