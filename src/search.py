from qdrant_client import QdrantClient
import numpy as np

client = QdrantClient(url="http://localhost:6333")


query_vector = np.random.rand(1536)
hits = client.search(
    collection_name="chats",
    query_vector=query_vector,
    limit=5  # Return 5 closest points
)
print(hits)