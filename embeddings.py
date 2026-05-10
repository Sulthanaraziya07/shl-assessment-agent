from sentence_transformers import SentenceTransformer
import json
import faiss
import numpy as np

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load catalog
with open("catalog.json", "r") as f:
    catalog = json.load(f)

# Extract names
texts = [item["name"] for item in catalog]

# Create embeddings
embeddings = model.encode(texts)

# Convert to numpy array
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# Save index
faiss.write_index(index, "shl_index.faiss")

# Save embeddings mapping
with open("mapping.json", "w") as f:
    json.dump(catalog, f, indent=2)

print("Embeddings and FAISS index created successfully!")