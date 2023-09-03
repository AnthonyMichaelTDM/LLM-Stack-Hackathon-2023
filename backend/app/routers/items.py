"""Feature routes."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..dependencies.items import (
    generate_text,
    make_error_message,
    WebSocketStreamingCallback,
)

router = APIRouter()


@router.websocket("/continue")
async def continue_websocket(websocket: WebSocket) -> None:
    """Websocket endpoint for continuing text."""
    await websocket.accept()
    stream_handler = WebSocketStreamingCallback(websocket)

    while True:
        try:
            response = await generate_text([stream_handler])
            await websocket.send_json(response.copy())
        except WebSocketDisconnect:
            break
        except Exception as e:
            error_payload = make_error_message(e)
            await websocket.send_json(error_payload)
            raise e
