import json
import math

import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
import uuid


client = QdrantClient(url="http://localhost:6333")
data_path = "./data/"
raw_path = data_path + "raw/"
embeddings_path = data_path + "embeddings/"
embedding_size = 1536  # ada-002


# Create a Qdrant collection for the chats
client.recreate_collection(
    collection_name="chats",
    vectors_config=VectorParams(size=embedding_size, distance=Distance.COSINE),
)

# Load the chats and embeddings
chats_df = pd.read_csv(raw_path + "chats.csv")
embeddings_df = pd.read_csv(embeddings_path + "chats-embeddings-ada-002.csv")

# Remove all chats that don't have embeddings
missing_embeddings_df = embeddings_df[embeddings_df["embedding"].isna()]
missing_embeddings_df_ids = missing_embeddings_df["thread_id"].tolist()
chats_df = chats_df[~chats_df["thread_id"].isin(missing_embeddings_df_ids)]
embeddings_df = embeddings_df[
    ~embeddings_df["thread_id"].isin(missing_embeddings_df_ids)
]

# # Load the messages and embeddings
# messages_df = pd.read_csv(raw_path + "messages.csv")
# messages_df_select = messages_df[messages_df["Channel_Name"]=="mlops-questions-answered" or messages_df["Channel_Name"]=="discussions"]
# message_embeddings_df = pd.read_csv(embeddings_path + "messages-embeddings-ada-002.csv")

# Upsert the chats into Qdrant
max_batch_size = 20
for i in range(
    math.ceil(len(embeddings_df) / max_batch_size)
):  # Upsert chats in batches
    client.upsert(
        collection_name="chats",
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=json.loads(vector),
                payload={
                    "thread_id": thread_id,
                    "chat_text": chat_text,
                },
            )
            for thread_id, vector, chat_text in zip(
                embeddings_df["thread_id"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
                embeddings_df["embedding"][
                    i * max_batch_size : (i + 1) * max_batch_size
                ],
                chats_df["chat_text"][i * max_batch_size : (i + 1) * max_batch_size],
            )
        ],
    )
