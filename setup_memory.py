import chromadb

# Create a ChromaDB client (local instance)
client = chromadb.PersistentClient(path="./chroma_db")

# Create a collection for our shared memory
collection = client.get_or_create_collection(name="shared_memory")

print("✅ Shared memory (ChromaDB) is ready!")