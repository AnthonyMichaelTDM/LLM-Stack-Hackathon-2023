import os
from typing import Any, List, Optional, Tuple

from dotenv import load_dotenv
import gradio as gr
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chains import MapReduceChain
from langchain.text_splitter import TextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.combine_documents.map_reduce import MapReduceDocumentsChain
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from threading import Lock
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, ScoredPoint, MatchValue

load_dotenv()

client = QdrantClient(url=os.getenv("QDRANT_URL"))

from langchain.schema import BaseMessage, AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

NUM_THEADS = 3
NUM_MESSAGES = 5

def load_qa_chain() -> ChatOpenAI:
    """Logic for loading the chain you want to use should go here."""
    llm = ChatOpenAI(
        temperature=0, model="gpt-4"
    )  # openai_organization=os.getenv('OPENAI_ORG_ID'), client=None
    # chain = ConversationChain(llm=llm)
    return llm

def load_sum_chain():
    """Logic for loading the chain you want to use should go here."""
    # base llm
    map_prompt = PromptTemplate(
        template = """You are a bot for summarizing wikipedia articles, you are terse and focus on accuracy.\n\nSummarize this text:\n{input}""",
        input_variables=["input"]
    )
    combine_prompt=PromptTemplate(
        template = """You are a diligent bot that summarizes text.\n\nPlease combine the articles below into one summary:\n{input}""",
        input_variables=["input"]
    )
    
    summarize = load_summarize_chain(llm=OpenAI(
            model="gpt-3.5-turbo"
        ),chain_type="map_reduce", verbose=False, map_prompt=map_prompt, combine_prompt=combine_prompt)
    
    return summarize

class ChatWrapper:
    def __init__(self) -> None:
        self.lock = Lock()

    def __call__(
        self,
        inp: str,
        history: Optional[List[Tuple[str, str]]],
    ) -> Tuple[Any, List[Tuple[str, str]]]:
        """Execute the chat functionality."""
        self.lock.acquire()
        
        try:
            history = history or []
            summarize = load_sum_chain()
            chat = load_qa_chain()

            messages: list[BaseMessage] = [
                SystemMessage(content="You are a helpful assistant."),
            ]
            for h in history:
                messages += [HumanMessage(content=h[0])]
                messages += [AIMessage(content=h[1])]

            query_vector = OpenAIEmbeddings().embed_query(inp)

            relevant_chats: List[ScoredPoint] = client.search(
                collection_name="chats",
                query_vector=query_vector,
                limit=NUM_THEADS,
            )

            thread_id = relevant_chats[0].payload["thread_id"]

            relevant_chats_text = [
                relevant_chats[i].payload["chat_text"]
                for i in range(len(relevant_chats))
            ]

            relevant_messages = client.search(
                collection_name="messages",
                query_vector=query_vector,
                query_filter=Filter(
                    must_not=[  # These conditions are required for search results
                        FieldCondition(
                            key="thread_id",  # Condition based on values of `rand_number` field.
                            match=MatchValue(value=thread_id),
                        )
                    ]
                ),
                limit=NUM_MESSAGES,
            )
            relevant_messages_text = [
                relevant_messages[i].payload["message_text"]
                for i in range(len(relevant_messages))
            ]

            messages += [
                AIMessage(
                    content="""
            [CONTEXT] Here is some context for the question.
            [RELEVANT MESSAGE THREADS]
            """
                    + "\n".join([text or "" for text in relevant_chats_text])
                    + """
            [RELEVANT MESSAGES]
            """
                    + "\n".join([text or "" for text in relevant_messages_text])
                )
            ]

            messages += [HumanMessage(content=inp)]
            
            # check if messages is too big for context window,
            # if so, map reduce each message that's above a certain threshold

            # Run chain and append input.
            output: str = chat(messages).content

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
        submit = gr.Button(value="Send", variant="secondary").style(full_width=False)

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

    submit.click(chat, inputs=[message, state, agent_state], outputs=[chatbot, state])
    message.submit(chat, inputs=[message, state, agent_state], outputs=[chatbot, state])

block.launch(debug=True)
