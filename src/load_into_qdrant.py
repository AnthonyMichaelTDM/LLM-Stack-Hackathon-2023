import json
import os
import math

from dotenv import load_dotenv
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
import uuid

load_dotenv()

client = QdrantClient(url=os.getenv("QDRANT_URL"))
chat_collection = "chats"
message_collection = "messages"
data_path = "./data/"
raw_path = data_path + "raw/"
embeddings_path = data_path + "embeddings/"
max_batch_size = 20  # max number of points to upsert at once to Qdrant

# Load the chats and embeddings
chats_df = pd.read_csv(raw_path + "chats.csv")
chats_embeddings_df = pd.read_csv(embeddings_path + "chats-embeddings-ada-002.csv")

# Load the messages and embeddings
messages_df = pd.read_csv(raw_path + "messages.csv")
messages_df_select = messages_df[
    (messages_df["Channel_Name"] == "mlops-questions-answered")
    | (messages_df["Channel_Name"] == "discussions")
]
messages_embeddings_df = pd.read_csv(
    embeddings_path + "messages-embeddings-ada-002-001.csv"
)


# Remove all chats that don't have embeddings
missing_chat_embeddings_df = chats_embeddings_df[
    chats_embeddings_df["embedding"].isna()
]
missing_chat_embeddings_df_ids = missing_chat_embeddings_df["thread_id"].tolist()
chats_df_select = chats_df[~chats_df["thread_id"].isin(missing_chat_embeddings_df_ids)]

chats_embeddings_df_ids = chats_embeddings_df["thread_id"].tolist()
chats_df_select = chats_df_select[
    chats_df_select["thread_id"].isin(chats_embeddings_df_ids)
]
chat_df_select_ids = chats_df_select["thread_id"].tolist()
chats_embeddings_df = chats_embeddings_df[
    chats_embeddings_df["thread_id"].isin(chat_df_select_ids)
]
chats_df_select = chats_df_select.reset_index(drop=True)
chats_embeddings_df = chats_embeddings_df.reset_index(drop=True)


# Remove all messages that don't have embeddings
missing_messages_embeddings_df = messages_embeddings_df[
    messages_embeddings_df["embedding"].isna()
]
missing_messages_embeddings_df_ids = missing_messages_embeddings_df["message_id"].tolist()
messages_df_select = messages_df_select[
    ~messages_df_select["Message_Timestamp"].isin(missing_messages_embeddings_df_ids)
]

messages_embeddings_df_ids = messages_embeddings_df["message_id"].tolist()
messages_df_select = messages_df_select[
    messages_df_select["Message_Timestamp"].isin(messages_embeddings_df_ids)
]
messages_df_select_ids = messages_df_select["Message_Timestamp"].tolist()
messages_embeddings_df = messages_embeddings_df[
    messages_embeddings_df["message_id"].isin(messages_df_select_ids)
]
messages_df_select = messages_df_select.reset_index(drop=True)
messages_embeddings_df = messages_embeddings_df.reset_index(drop=True)


# Create two qdrant collections for the chats + messages
chat_embedding_size = len(json.loads(chats_embeddings_df["embedding"][0]))
message_embedding_size = len(json.loads(messages_embeddings_df["embedding"][0]))

client.recreate_collection(
    collection_name=chat_collection,
    vectors_config=VectorParams(size=chat_embedding_size, distance=Distance.COSINE),
)
client.recreate_collection(
    collection_name=message_collection,
    vectors_config=VectorParams(size=message_embedding_size, distance=Distance.COSINE),
)

# Upsert the chats into Qdrant
for i in range(
    math.ceil(len(chats_embeddings_df) / max_batch_size)
):  # Upsert chats in batches
    client.upsert(
        collection_name=chat_collection,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=json.loads(vector),
                payload={
                    "thread_id": thread_id,
                    "channel_name": channel_name,
                    "chat_text": chat_text,
                },
            )
            for vector, thread_id, channel_name, chat_text in zip(
                chats_embeddings_df["embedding"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
                chats_embeddings_df["thread_id"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
                chats_df_select["channel_name"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
                chats_df_select["chat_text"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
            )
        ],
    )
for i in range(
    math.ceil(len(messages_embeddings_df) / max_batch_size)
):  # Upsert chats in batches
    client.upsert(
        collection_name=message_collection,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=json.loads(vector),
                payload={
                    "thread_id": thread_id,
                    "channel_name": channel_name,
                    "message_text": message_text,
                },
            )
            for vector, thread_id, channel_name, message_text in zip(
                messages_embeddings_df["embedding"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
                messages_df_select["Thread_Timstamp"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
                messages_df_select["Channel_Name"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
                messages_df_select["__Text"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
            )
        ],
    )
