# crea le colleciton per chromadb richiamando VectorStore
import chormadb

client = chormadb.PersistenClient(
    path="./data/chroma"
)

client.get_or_create_collection(
    name="database_schema"
)

print("Vector database initialized")
