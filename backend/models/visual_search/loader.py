import numpy as np
from PIL import Image
from keras.applications import ResNet50
from keras.applications.resnet import preprocess_input

class ResNet50TFExtractor:
    def __init__(self):
        self.model = ResNet50(weights="imagenet", include_top=False, pooling="avg")
    
    def image_to_embedding(self, pil_image: Image.Image):
        img = pil_image.resize((224, 224))
        arr = np.array(img).astype(np.float32)
        if arr.ndim == 2:
            arr = np.stack([arr]*3, axis=-1)
        # Convertir a RGB si tiene 4 canales (PNG transparente)
        if arr.shape[-1] == 4:
            arr = arr[..., :3]
            
        arr = np.expand_dims(arr, axis=0)
        arr = preprocess_input(arr)
        
        emb = self.model.predict(arr, verbose=0)
        emb = emb.reshape(-1).astype(np.float32)
        
        norm = np.linalg.norm(emb) + 1e-10
        emb = emb / norm
        return emb