"""API endpoints for the chatbot."""
from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse

from ..dependencies import ChatRequest, create_chat_response

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
async def chat(data: ChatRequest) -> StreamingResponse:
    """Chat with the AI.

    Parameters
    ----------
    data : ChatRequest
        Chat request

    Returns
    -------
    StreamingResponse
        Response from the AI
    """
    return StreamingResponse(
        create_chat_response(data.user_id, data.conversation_id, data.message),
        media_type="text/event-stream",
    )
