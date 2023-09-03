"""Dependencies for items endpoints."""
import os
from typing import Any

from fastapi import WebSocket
from langchain import LLMChain, PromptTemplate
from langchain.callbacks.base import AsyncCallbackHandler, Callbacks
from langchain.chat_models import ChatOpenAI
from starlette.websockets import WebSocketState


# Models
class WebSocketStreamingCallback(AsyncCallbackHandler):
    """Callback handler for streaming LLM responses."""

    def __init__(self, websocket: WebSocket):
        self.websocket = websocket

    async def on_llm_new_token(self, token: str, **_: Any) -> None:
        """Run when LLM generates a new token."""
        payload = {"message": token}
        if self.websocket.client_state == WebSocketState.CONNECTED:
            await self.websocket.send_json(payload)


# Helper fns
def create_llm(
    callbacks: Callbacks = None, model: str = "gpt-3.5-turbo", temperature: float = 0.9, max_tokens: int = 100
):
    """Create an LLM instance."""
    return ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        streaming=bool(callbacks),
        callbacks=callbacks,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def create_prompt(
    input_vars=None,
    template: str = "Do not write anything more than what is asked, and do what is asked using three sentences at most: {text}",
) -> PromptTemplate:
    """Create a prompt template."""
    return PromptTemplate(
        input_variables=input_vars,
        template=template,
    )


async def generate_text(
    callbacks: Callbacks = None,
    text: str = "Write an extremely unknown but interesting fact, explaining the origins, significance, and more.",
) -> dict[str, str]:
    try:
        llm = create_llm(callbacks)
        prompt = create_prompt(["text"])
        chain = LLMChain(llm=llm, prompt=prompt)
        result = await chain.arun(text)
        data = {"result": result, "status": "DONE"}
        return data
    except Exception as e:
        raise e


def make_error_message(e: Exception) -> dict[str, str]:
    error_message = {
        "status": "ERROR",
        "error_message": repr(e),
    }
    return error_message
