import os
import numpy as np
import faiss
from .utils import load_embeddings_npy, load_metadata_json

class VisualSearchEngine:
    def __init__(self, embeddings_path, metadata_path, index_path=None):
        self.emb_path = embeddings_path
        self.meta_path = metadata_path
        self.index_path = index_path or os.path.splitext(self.emb_path)[0] + ".faiss"

        self.embeddings = load_embeddings_npy(self.emb_path)
        self.metadata = load_metadata_json(self.meta_path)
        self.d = self.embeddings.shape[1]

        # Cargar o crear index FAISS
        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
                print("Index FAISS cargado correctamente.")
            except Exception as e:
                print("Error leyendo index, recreando...", e)
                self.index = None
        else:
            self.index = None

        if self.index is None:
            self.index = faiss.IndexFlatIP(self.d)
            self.index.add(self.embeddings)
            try:
                faiss.write_index(self.index, self.index_path)
            except Exception as e:
                print("No se pudo guardar el index:", e)

    def search(self, query_embedding, top_k=5):
        # ... (código anterior de normalización se mantiene igual) ...
        q = np.array(query_embedding, dtype=np.float32).reshape(1, -1)
        faiss.normalize_L2(q)

        sims, idxs = self.index.search(q, top_k)
        sims = sims[0]
        idxs = idxs[0]

        results = []
        for score, idx in zip(sims, idxs):
            if idx < 0 or idx >= len(self.metadata):
                continue
            item = self.metadata[idx]
            
            # --- AQUÍ ESTÁ LA CORRECCIÓN ---
            # Leemos 'image_path' del JSON, pero lo enviamos como 'image_url' al frontend
            img_link = item.get("image_path") or item.get("image_url") or item.get("link")
            
            results.append({
                "product_id": item.get("id"),
                "name": item.get("productDisplayName") or item.get("name"),
                "image_url": img_link,  
                "similarity": float(score),
                "category": item.get("articleType"),
                "price": item.get("price") 
            })
        return results