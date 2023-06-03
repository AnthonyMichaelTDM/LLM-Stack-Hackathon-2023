import json
import pandas as pd
from tqdm import tqdm

data_path = "./data/"
raw_path = data_path + "raw/"
embeddings_path = data_path + "embeddings/"

messages_df = pd.read_csv(raw_path + "messages.csv")
df_mlops_questions_answered = messages_df[messages_df["Channel_Name"]=="mlops-questions-answered"]
df_discussions = messages_df[messages_df["Channel_Name"]=="discussions"]
message_embeddings_df = pd.read_csv(embeddings_path + "messages-embeddings-ada-002.csv")

chats_df = pd.read_csv(raw_path + "chats.csv")
embeddings_df = pd.read_csv(embeddings_path + "chats-embeddings-ada-002.csv")

# Create a temp index of the chats
chats_index = {}
for _, row in tqdm(chats_df.iterrows(), desc="Creating temporary chats index"):
  chats_index[row['thread_id']] = row['chat_text']

# Link the chats and embeddings together
embeddings = []
VECTOR_SIZE = None
for _, row in tqdm(embeddings_df.iterrows(), desc="Collecting chats and embeddings"):
  embedding = json.loads(row['embedding'])
  embeddings.append({"thread_id": row['thread_id'], "embedding":  embedding})
  if not VECTOR_SIZE:
    VECTOR_SIZE = len(embedding)
  else:
    assert VECTOR_SIZE==len(embedding)



from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
max_num_chunks = (
20  # TODO: Find optimal number of chunks to upsert at once
)
for i in range(
math.ceil(len(extracted_chunks) / max_num_chunks)
):  # Upsert chunks in batches
    qdrantClient.upsert(
        collection_name=qdrant_collection,
        points=[
            PointStruct(
                id=chunk_id,
                vector=vector,
                payload={
                    "resource_pid": resource_pid,
                    "chunk": chunk,
                },
            )
            for chunk_id, chunk, vector in zip(
                chunk_ids[
                    i * max_num_chunks : (i + 1) * max_num_chunks
                ],
                extracted_chunks[
                    i * max_num_chunks : (i + 1) * max_num_chunks
                ],
                embeddings[
                    i * max_num_chunks : (i + 1) * max_num_chunks
                ],
            )
        ],
    )