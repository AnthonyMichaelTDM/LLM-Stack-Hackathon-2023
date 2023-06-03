import json
import math

import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
import uuid


client = QdrantClient(url="http://localhost:6334")
chat_collection = "chats"
message_collection = "messages"
data_path = "./data/"
raw_path = data_path + "raw/"
embeddings_path = data_path + "embeddings/"
embedding_size = 1536  # ada-002


# Create two qdrant collections for the chats + messages
client.recreate_collection(
    collection_name=chat_collection,
    vectors_config=VectorParams(size=embedding_size, distance=Distance.COSINE),
)
client.recreate_collection(
    collection_name=message_collection,
    vectors_config=VectorParams(size=embedding_size, distance=Distance.COSINE),
)


# Load the chats and embeddings
chats_df = pd.read_csv(raw_path + "chats.csv")
chats_embeddings_df = pd.read_csv(embeddings_path + "chats-embeddings-ada-002.csv")

# Load the messages and embeddings
messages_df = pd.read_csv(raw_path + "messages.csv")
messages_df_select = messages_df[(messages_df["Channel_Name"]=="mlops-questions-answered") & (messages_df["Channel_Name"]=="discussions")]
message_embeddings_df = pd.read_csv(embeddings_path + "messages-embeddings-ada-002-001.csv")


# Remove all chats that don't have embeddings
missing_chat_embeddings_df = chats_embeddings_df[chats_embeddings_df["embedding"].isna()]
missing_chat_embeddings_df_ids = missing_chat_embeddings_df["thread_id"].tolist()
chats_df_select = chats_df[~chats_df["thread_id"].isin(missing_chat_embeddings_df_ids)]
chats_embeddings_df = chats_embeddings_df[
    ~chats_embeddings_df["thread_id"].isin(missing_chat_embeddings_df_ids)
]

# Remove all messages that don't have embeddings
missing_message_embeddings_df = message_embeddings_df[message_embeddings_df["embedding"].isna()]
missing_message_embeddings_df_ids = missing_message_embeddings_df["message_id"].tolist()
messages_df_select = messages_df_select[~messages_df_select["Message_Timestamp"].isin(missing_message_embeddings_df_ids)]
messages_df_select_ids = messages_df_select["Message_Timestamp"].tolist()
message_embeddings_df = message_embeddings_df[
    message_embeddings_df["message_id"].isin(messages_df_select_ids)
]

# Upsert the chats into Qdrant
max_batch_size = 20

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
                    "chat_text": chat_text,
                },
            )
            for vector, thread_id, chat_text in zip(
                chats_embeddings_df["embedding"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
                chats_embeddings_df["thread_id"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
                chats_df_select["chat_text"][i * max_batch_size : (i + 1) * max_batch_size],
            )
        ],
    )
for i in range(
    math.ceil(len(message_embeddings_df) / max_batch_size)
):  # Upsert chats in batches
    client.upsert(
        collection_name=message_collection,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=json.loads(vector),
                payload={
                    "thread_id": thread_id,
                    "message_text": message_text,
                },
            )
            for vector, thread_id, message_text in zip(
                message_embeddings_df["embedding"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
                messages_df_select["Thread_Timstamp"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
                messages_df_select["__Text"][i * max_batch_size : (i + 1) * max_batch_size],
            )
        ],
    )
