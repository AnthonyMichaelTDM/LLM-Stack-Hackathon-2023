"""API endpoints for the chatbot."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from ..dependencies import ChatRequest, create_chat_response, get_current_active_user, User

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


@router.post("/chat/", response_class=StreamingResponse)
async def chat(current_user: Annotated[User, Depends(get_current_active_user)], data: ChatRequest) -> StreamingResponse:
    """Chat with the AI.

    Parameters
    ----------
    current_user : User
        Current user
    data : ChatRequest
        Chat request

    Returns
    -------
    StreamingResponse
        Response from the AI

    Raises
    ------
    HTTPException
        If OpenAI fails
    """
    try:
        return StreamingResponse(
            create_chat_response(current_user, data.conversation_id, data.message),
            media_type="text/event-stream",
        )
    except Exception:
        raise HTTPException(status_code=400, detail="OpenAI failure")
