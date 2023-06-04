import os
from typing import List

from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, ScoredPoint, MatchValue
from langchain.schema import BaseMessage, AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv

client = QdrantClient(url=os.getenv("QDRANT_URL"))
load_dotenv()

NUM_THEADS = 3
NUM_MESSAGES = 5

def qa(inp:str) -> str:
    # summarize = load_sum_chain()
    chat = ChatOpenAI(
        temperature=0, model="gpt-3.5-turbo"
    )  # openai_organization=os.getenv('OPENAI_ORG_ID'), client=None

    messages: list[BaseMessage] = [
        SystemMessage(
            content="""
        You are a kind, helpful, knowledgable chatbot that specializes in answering questions about machine learning. Sometimes, we will provide you with the relevant context to answer the question. 

        This is a question-answering system over a corpus of chats from the MLOps Community, a group of machine learning enthusiasts.
        Given multiple message threads, messages, and a question, create an answer to the question that references those chats as "SOURCES" citing the channel name and message. Avoid any channel or user ids.

        - If the question asks about the system's capabilities, the system should respond with some version of "This system can answer questions about machine learning from the MLOps Slack community.”. The answer does not need to include sources.
        - If the answer cannot be determined from the message threads or from these instructions, the system should not answer the question. The system should instead return "No relevant sources found" and ask for clarification.
        - Sources are not guaranteed to be relevant to the question."""
        ),
    ]

    query_vector = OpenAIEmbeddings().embed_query(inp)

    relevant_chats: List[ScoredPoint] = client.search(
        collection_name="chats",
        query_vector=query_vector,
        limit=NUM_THEADS,
    )
    thread_id = relevant_chats[0].payload["thread_id"]
    relevant_chats_channel_names = [
        relevant_chats[i].payload["channel_name"]
        for i in range(len(relevant_chats))
    ]
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
    relevant_messages_channel_names = [
        relevant_messages[i].payload["channel_name"]
        for i in range(len(relevant_messages))
    ]
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
            + "\n\n\n\n\n".join(
                [
                    "From channel: " + channel_name + "\n" + text
                    for channel_name, text in zip(
                        relevant_chats_channel_names, relevant_chats_text
                    )
                ]
            )
            + """
    [RELEVANT MESSAGES]
    """
            + "\n\n\n\n\n".join(
                [
                    "From channel: " + channel_name + "\n" + text
                    for channel_name, text in zip(
                        relevant_messages_channel_names, relevant_messages_text
                    )
                ]
            )
        )
    ]

    messages += [HumanMessage(content=inp)]

    # check if messages is too big for context window,
    # if so, map reduce each message that's above a certain threshold

    # Run chain and append input.
    output: str = chat(messages).content

    return output

import numpy as np
import pandas as pd
from multiprocessing import Pool

NUM_CORES = 8

def gen_answers( df: pd.DataFrame) -> pd.DataFrame:
    df["answers"] = df["answer"].apply(qa)
    
    return df

def test_all_questions():
    data = pd.read_csv("data/questions_list.csv")
    pool = Pool(NUM_CORES)
    df_split = np.array_split(data, NUM_CORES)
    
    data = pd.concat(pool.map(gen_answers, df_split))
    
    pool.close()
    pool.join()
        
    data.to_csv("data/questions_with_answers.csv")
    
def __main__():
    test_all_questions()

if __main__():
    __main__()