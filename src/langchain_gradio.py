import os
from typing import Optional, Tuple

import gradio as gr
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
from threading import Lock
from dotenv import load_dotenv

load_dotenv()


def load_chain():
    """Logic for loading the chain you want to use should go here."""
    llm = OpenAI(temperature=0)
    chain = ConversationChain(llm=llm)
    return chain


class ChatWrapper:
    def __init__(self):
        self.lock = Lock()

    def __call__(
        self, inp: str, history: Optional[Tuple[str, str]], chain: Optional[ConversationChain]
    ):
        """Execute the chat functionality."""
        self.lock.acquire()
        try:
            history = history or []
            chain = load_chain()

            # Run chain and append input.
            output = chain.run(input=inp)
            history.append((inp, output))
        except Exception as e:
            raise e
        finally:
            self.lock.release()
        return history, history


chat = ChatWrapper()

block = gr.Blocks(css=".gradio-container ")  # {background-color: lightgray}

with block:
    with gr.Row():
        gr.Markdown("<h3><center>SF LLM Stack Hackathon - Team Good Bing</center></h3>")

    chatbot = gr.Chatbot()

    with gr.Row():
        message = gr.Textbox(
            label="What's your question?",
            placeholder="What's the answer to life, the universe, and everything?",
            lines=1,
        )
        submit = gr.Button(value="Send", variant="secondary").style(
            full_width=False)

    gr.Examples(
        examples=[
            "What is machine learning for a 11 year old?",
            "Why is 42 the meaning of life?",
            "Top 3 tricky questions for OpenAI chatbot?",
        ],
        inputs=message,
    )


    gr.HTML(
        "<center><a target='_blank' href='https://github.com/AnthonyMichaelTDM/LLM-Stack-Hackathon-2023'>GitHub Repo</a>; Powered by <a href='https://github.com/hwchase17/langchain'>LangChain 🦜️🔗</a></center>"
    )

    state = gr.State()
    agent_state = gr.State()

    submit.click(chat, inputs=[message, state,
                 agent_state], outputs=[chatbot, state])
    message.submit(chat, inputs=[message, state,
                   agent_state], outputs=[chatbot, state])

block.launch(debug=True)
