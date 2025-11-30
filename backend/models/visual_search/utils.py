import numpy as np
import json

def load_embeddings_npy(npy_path):
    emb = np.load(npy_path)
    if emb.dtype != np.float32:
        emb = emb.astype(np.float32)
    # Normalizar
    norms = np.linalg.norm(emb, axis=1, keepdims=True) + 1e-10
    emb = emb / norms
    return emb

def load_metadata_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return meta