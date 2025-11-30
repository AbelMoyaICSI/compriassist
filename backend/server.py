"""
ComprIAssist - Servidor Principal
Asistente Inteligente de Compras de Productos E-commerce basado en IA

Este es el servidor backend que orquesta los 5 módulos de IA para
gestión inteligente de catálogos de productos de tiendas online.
"""

import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles 
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from PIL import Image

# ============================================
# IMPORTACIONES DE MÓDULOS PROPIOS
# ============================================

# Módulo Chatbot
from models.chatbot import create_chatbot

# Módulo Sentiment (con sus dependencias)
from models.sentiment import SentimentModel, FraudDetector
try:
    from pysentimiento import create_analyzer 
    PYSENTIMIENTO_AVAILABLE = True
except ImportError:
    PYSENTIMIENTO_AVAILABLE = False

# Módulo Visual Search (CNN)
try:
    from models.visual_search.loader import ResNet50TFExtractor
    from models.visual_search.engine import VisualSearchEngine
    VISUAL_SEARCH_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Módulo de Visión no disponible: {e}")
    VISUAL_SEARCH_AVAILABLE = False

# Módulo Generativo (NUEVO)
try:
    from models.generative.api_endpoint import setup_generative_routes
    GENERATIVE_AVAILABLE = True
    print("✅ Módulo generativo disponible")
except ImportError as e:
    GENERATIVE_AVAILABLE = False
    print(f"⚠️ Módulo generativo no disponible: {e}")

# ============================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================

app = FastAPI(
    title="ComprIAssist API",
    description="API para Asistente Inteligente de Compras de Productos E-commerce con 5 Módulos de IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# INICIALIZACIÓN DE MODELOS (AL ARRANQUE)
# ============================================

# Executor para no bloquear el loop principal con tareas pesadas (CPU/GPU)
thread_pool = ThreadPoolExecutor(max_workers=1)

# Variables globales para los modelos
extractor = None
search_engine = None

# Inicializar Chatbot
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY", None)
chatbot = create_chatbot(hf_api_key=HF_API_KEY)

print("✅ Chatbot inicializado correctamente")
if HF_API_KEY:
    print("   → Usando HuggingFace API para respuestas avanzadas")
else:
    print("   → Usando respuestas predefinidas (configura HUGGINGFACE_API_KEY para mejores respuestas)")

# Inicializar Sentiment Analysis
sentiment_model = SentimentModel()
fraud_detector = FraudDetector()
print("✅ Módulo de análisis de sentimientos inicializado")

# Inicializar Visual Search
if VISUAL_SEARCH_AVAILABLE:
    print("--- Cargando modelos de Visión Artificial... ---")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    
    # Definir las 3 rutas explícitamente
    EMB_PATH = os.path.join(DATA_DIR, "embeddings_resnet50.npy")
    META_PATH = os.path.join(DATA_DIR, "metadata_resnet50_cloudinary.json")
    FAISS_PATH = os.path.join(DATA_DIR, "embeddings_resnet50.faiss")
    
    # Comprobar que existan
    if os.path.exists(EMB_PATH) and os.path.exists(META_PATH) and os.path.exists(FAISS_PATH):
        try:
            extractor = ResNet50TFExtractor()
            search_engine = VisualSearchEngine(EMB_PATH, META_PATH, index_path=FAISS_PATH)
            print(f"✅ Modelos de visión cargados. Index usado: {FAISS_PATH}")
        except Exception as e:
            print(f"❌ ERROR cargando modelos de visión: {e}")
    else:
        print(f"⚠️ FALTAN ARCHIVOS en {DATA_DIR}. Verifica .npy, .json y .faiss")

# Integrar módulo generativo
if GENERATIVE_AVAILABLE:
    setup_generative_routes(app)
    print("✅ Módulo generativo integrado exitosamente")
else:
    print("⚠️ Módulo generativo no integrado")

# ============================================
# MODELOS DE DATOS (Pydantic)
# ============================================

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None

class SentimentRequest(BaseModel):
    text: str

class RecommendationRequest(BaseModel):
    user_id: str
    context: Optional[str] = None
    limit: int = 10

class GenerativeRequest(BaseModel):
    product_name: str
    category: str
    style: Optional[str] = "formal"

# ============================================
# ENDPOINTS DE SALUD
# ============================================

@app.get("/")
async def root():
    """Endpoint raíz - Información de la API"""
    return {
        "name": "ComprIAssist API",
        "version": "1.0.0",
        "description": "Asistente Inteligente de Compras de Productos E-commerce basado en IA",
        "status": "operational",
        "modules": {
            "chatbot": "ready ✅",
            "generative": "ready ✅" if GENERATIVE_AVAILABLE else "not available ⚠️",
            "sentiment": "ready ✅",
            "visual_search": "active ✅" if search_engine else "inactive ⚠️ (check logs)",
            "recommendation": "in development 🚧"
        },
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "chatbot": "/api/chatbot/message",
            "sentiment": "/api/sentiment/analyze",
            "visual_search": "/api/visual/search",
            "generative": "/api/generative/" if GENERATIVE_AVAILABLE else "not available",
            "recommendation": "/api/recommend/products"
        }
    }

@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": "2025-11-29",
        "modules": {
            "chatbot": True,
            "generative": GENERATIVE_AVAILABLE,
            "sentiment": True,
            "visual_search": search_engine is not None,
            "recommendation": False  # En desarrollo
        }
    }

# ============================================
# MÓDULO 1: CHATBOT
# ============================================

@app.post("/api/chatbot/message")
async def chatbot_message(chat: ChatMessage):
    """
    Procesa un mensaje del usuario y retorna respuesta del chatbot
    
    Funcionalidades:
    - Detección de intenciones con clasificador basado en reglas
    - Extracción de entidades (productos, colores, tallas, precios)
    - Generación de respuestas contextuales
    - Sugerencias de acciones
    """
    try:
        # Validar que el mensaje no esté vacío
        if not chat.message or len(chat.message.strip()) == 0:
            raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")
        
        # Procesar mensaje con el chatbot
        result = chatbot.process_message(
            message=chat.message,
            user_id=chat.user_id
        )
        
        return {
            "response": result["response"],
            "intent": result["intent"],
            "confidence": result["confidence"],
            "entities": result["entities"],
            "suggestions": result["suggestions"],
            "timestamp": "2025-11-29"
        }
    
    except Exception as e:
        print(f"Error en chatbot: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar mensaje: {str(e)}")

# ============================================
# MÓDULO 2: RECOMENDACIÓN
# ============================================

@app.post("/api/recommend/products")
async def recommend_products(request: RecommendationRequest):
    """
    Genera recomendaciones personalizadas de productos
    
    TODO: Implementar:
    - Random Forest classifier
    - K-means clustering
    - Filtrado colaborativo
    """
    return {
        "user_id": request.user_id,
        "recommendations": [
            {"product_id": 1, "name": "Producto Ejemplo 1", "score": 0.95},
            {"product_id": 2, "name": "Producto Ejemplo 2", "score": 0.87},
        ],
        "algorithm": "random_forest",
        "total_found": 2,
        "status": "simulation"
    }

# ============================================
# MÓDULO 3: ANÁLISIS DE SENTIMIENTOS
# ============================================

@app.post("/api/sentiment/analyze")
async def analyze_sentiment(request: SentimentRequest):
    """
    Analiza el sentimiento de una reseña y detecta si es potencialmente falsa.
    """
    
    # 1. Análisis de Sentimiento (pysentimiento o respaldo)
    sentiment_result = sentiment_model.analyze(request.text)

    # 2. Detección de Reseña Falsa (basado en patrones)
    fraud_result = fraud_detector.analyze(request.text)
    
    # 3. Combinar y devolver los resultados
    return {
        "text": request.text,
        "sentiment": sentiment_result["sentiment"],
        "confidence": sentiment_result["confidence"],
        "probabilities": sentiment_result["probabilities"],
        "is_fake": fraud_result["is_fake"],
        "fake_probability": fraud_result["fake_probability"]
    }

# ============================================
# MÓDULO 4: BÚSQUEDA VISUAL
# ============================================

@app.post("/api/visual/search")
async def visual_search(file: UploadFile = File(...), top_k: int = 5):
    """
    Búsqueda de productos similares por imagen utilizando ResNet50 + FAISS
    """
    if not search_engine or not extractor:
        raise HTTPException(
            status_code=503, 
            detail="El servicio de búsqueda visual no está disponible (modelos no cargados)."
        )

    # 1. Validar imagen
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen.")

    try:
        content = await file.read()
        pil_image = Image.open(BytesIO(content)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Archivo de imagen corrupto o inválido.")

    # 2. Generar embedding (CPU/GPU intensivo) -> Ejecutar en thread pool
    # Esto evita que el servidor se congele para otros usuarios
    loop = asyncio.get_event_loop()
    try:
        query_emb = await loop.run_in_executor(
            thread_pool, 
            extractor.image_to_embedding, 
            pil_image
        )
    except Exception as e:
        print(f"Error en inferencia: {e}")
        raise HTTPException(status_code=500, detail="Error procesando la imagen con la IA.")

    # 3. Buscar en FAISS
    results = search_engine.search(query_emb, top_k=top_k)

    return {
        "filename": file.filename,
        "total_found": len(results),
        "similar_products": results
    }

# ============================================
# MÓDULO 5: IA GENERATIVA (INTEGRADO)
# ============================================

# Los endpoints del módulo generativo se agregan automáticamente
# a través de setup_generative_routes(app)
#
# Endpoints disponibles:
# - POST /api/generative/generar-descripcion
# - POST /api/generative/chatbot-respuesta
# - POST /api/generative/generar-titulo-seo
# - POST /api/generative/generar-batch
# - GET  /api/generative/templates
# - GET  /api/generative/health

# ============================================
# MANEJO DE ERRORES
# ============================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Manejo global de errores"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "detail": "Ha ocurrido un error en el servidor"
        }
    )

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 COMPRIASSIST - SERVIDOR BACKEND")
    print("="*70)
    print(f"\n✅ Módulos cargados:")
    print(f"   • Chatbot: ✅")
    print(f"   • IA Generativa: {'✅' if GENERATIVE_AVAILABLE else '⚠️ No disponible'}")
    print(f"   • Análisis de Sentimientos: ✅")
    print(f"   • Búsqueda Visual: {'✅' if search_engine else '⚠️ No disponible (faltan datos)'}")
    print(f"   • Recomendación: 🚧 En desarrollo")
    print(f"\n📖 Documentación: http://localhost:8000/docs")
    print(f"🔗 API Root: http://localhost:8000/")
    print("="*70 + "\n")
    
    # Asegúrate de crear la carpeta data si no existe
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "data")):
        print("⚠️ NOTA: Crea la carpeta 'backend/data' y coloca tus .npy, .json y .faiss ahí.")
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

"""
INSTRUCCIONES DE USO:

1. Instalar dependencias:
   pip install -r requirements.txt

2. Configurar variables de entorno (.env):
   HUGGINGFACE_API_KEY=tu_token_aqui
   HUGGINGFACE_TOKEN_GENERATIVE=tu_token_generativo

3. Ejecutar servidor:
   python backend/server.py

4. Acceder a documentación interactiva:
   http://localhost:8000/docs

5. Endpoints disponibles:
   
   CHATBOT (Funcional):
   - POST /api/chatbot/message
   
   IA GENERATIVA (Funcional):
   - POST /api/generative/generar-descripcion
   - POST /api/generative/chatbot-respuesta
   - POST /api/generative/generar-titulo-seo
   - POST /api/generative/generar-batch
   - GET  /api/generative/templates
   - GET  /api/generative/health
   
   ANÁLISIS DE SENTIMIENTOS (Funcional):
   - POST /api/sentiment/analyze
   
   BÚSQUEDA VISUAL (Funcional si hay datos):
   - POST /api/visual/search
   
   EN DESARROLLO:
   - POST /api/recommend/products

MÓDULOS IMPLEMENTADOS:
- ✅ Módulo 1: Chatbot con NLU
- ✅ Módulo 2: Análisis de Sentimientos + Detección de Fraude
- ✅ Módulo 3: Búsqueda Visual (ResNet50 + FAISS)
- ✅ Módulo 4: IA Generativa (Templates + HuggingFace)
- 🚧 Módulo 5: Sistema de Recomendación (En desarrollo)

PRÓXIMOS PASOS:
- ✅ Fusionar todos los módulos
- 🚧 Implementar sistema de recomendación
- 🚧 Conectar con base de datos
- 🚧 Añadir autenticación
- 🚧 Añadir rate limiting
- 🚧 Despliegue en producción
"""