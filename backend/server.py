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
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
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

# Módulo Generativo (INTEGRADO DIRECTAMENTE)
try:
    from models.generative.generative_model import GenerativeModel
    from models.generative.prompt_templates import PromptTemplates
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
generative_model = None

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

# Inicializar modelo generativo
if GENERATIVE_AVAILABLE:
    generative_model = GenerativeModel()
    print("✅ Módulo generativo inicializado exitosamente")

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

# Modelos para IA Generativa
class CategoriaProducto(str, Enum):
    """Categorías de productos disponibles."""
    ROPA = "ropa"
    ELECTRONICA = "electronica"
    HOGAR = "hogar"
    DEPORTES = "deportes"
    BELLEZA = "belleza"
    ALIMENTOS = "alimentos"
    JUGUETES = "juguetes"
    LIBROS = "libros"
    GENERAL = "general"

class GenerarDescripcionRequest(BaseModel):
    """Request para generar descripción de producto."""
    nombre_producto: str = Field(..., description="Nombre del producto", min_length=3)
    caracteristicas: Optional[List[str]] = Field(None, description="Lista de características")
    categoria: Optional[CategoriaProducto] = Field(None, description="Categoría del producto")
    precio: Optional[float] = Field(None, description="Precio del producto", gt=0)
    max_tokens: int = Field(150, description="Máximo de tokens", ge=50, le=300)
    temperatura: float = Field(0.7, description="Temperatura de generación", ge=0.0, le=1.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre_producto": "Camiseta de algodón orgánico",
                "caracteristicas": ["100% algodón", "Talla M", "Eco-friendly"],
                "categoria": "ropa",
                "precio": 29.99,
                "temperatura": 0.7
            }
        }

class ChatbotGenerativoRequest(BaseModel):
    """Request para generar respuesta de chatbot."""
    pregunta: str = Field(..., description="Pregunta del usuario", min_length=3)
    contexto: Optional[str] = Field(None, description="Contexto de la conversación")
    max_tokens: int = Field(200, description="Máximo de tokens", ge=50, le=400)
    
    class Config:
        json_schema_extra = {
            "example": {
                "pregunta": "¿Tienen ropa para verano?",
                "contexto": "El usuario busca ropa casual"
            }
        }

class TituloSEORequest(BaseModel):
    """Request para generar título SEO."""
    nombre_base: str = Field(..., description="Nombre base del producto")
    caracteristicas: Optional[List[str]] = Field(None, description="Características destacadas")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre_base": "Zapatillas deportivas",
                "caracteristicas": ["Running", "Amortiguación", "Transpirables"]
            }
        }

class GenerarBatchRequest(BaseModel):
    """Request para generar múltiples descripciones."""
    productos: List[Dict[str, Any]] = Field(..., description="Lista de productos")
    
    class Config:
        json_schema_extra = {
            "example": {
                "productos": [
                    {
                        "nombre_producto": "Producto 1",
                        "caracteristicas": ["Característica 1", "Característica 2"]
                    },
                    {
                        "nombre_producto": "Producto 2",
                        "caracteristicas": ["Feature A", "Feature B"]
                    }
                ]
            }
        }

# ============================================
# DEPENDENCY PARA MODELO GENERATIVO
# ============================================

def get_generative_model():
    """Dependency para obtener instancia del modelo generativo."""
    if not GENERATIVE_AVAILABLE or generative_model is None:
        raise HTTPException(
            status_code=503, 
            detail="El módulo generativo no está disponible"
        )
    return generative_model

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
            "generative": "/api/generative/",
            "recommendation": "/api/recommend/products"
        }
    }

@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
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
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        print(f"Error en chatbot: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al procesar mensaje: {str(e)}")

# ============================================
# MÓDULO 2: ANÁLISIS DE SENTIMIENTOS
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
# MÓDULO 3: BÚSQUEDA VISUAL
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
# MÓDULO 4: IA GENERATIVA (INTEGRADO)
# ============================================

@app.get("/api/generative/")
async def info_generativa():
    """
    Información general del módulo de IA Generativa.
    """
    return {
        "modulo": "IA Generativa",
        "version": "1.0.0",
        "descripcion": "Generación automática de contenido para productos",
        "tecnologias": ["Hugging Face", "Templates Inteligentes"],
        "endpoints": [
            "/api/generative/generar-descripcion",
            "/api/generative/chatbot-respuesta",
            "/api/generative/generar-titulo-seo",
            "/api/generative/generar-batch",
            "/api/generative/templates",
            "/api/generative/health"
        ],
        "estado": "Operativo ✅" if GENERATIVE_AVAILABLE else "No disponible ⚠️"
    }

@app.post("/api/generative/generar-descripcion")
async def generar_descripcion(
    request: GenerarDescripcionRequest,
    model: GenerativeModel = Depends(get_generative_model)
):
    """
    Genera una descripción atractiva para un producto.
    
    *Parámetros:*
    - *nombre_producto*: Nombre del producto (requerido)
    - *caracteristicas*: Lista de características principales
    - *categoria*: Categoría del producto (ropa, electrónica, etc.)
    - *precio*: Precio del producto
    - *temperatura*: Nivel de creatividad (0.0-1.0)
    
    *Retorna:*
    - Descripción generada
    - Metadatos del proceso
    """
    try:
        resultado = model.generar_descripcion_producto(
            nombre_producto=request.nombre_producto,
            caracteristicas=request.caracteristicas,
            categoria=request.categoria.value if request.categoria else None,
            precio=request.precio,
            max_tokens=request.max_tokens,
            temperatura=request.temperatura
        )
        
        return {
            "success": True,
            "data": resultado,
            "message": "Descripción generada exitosamente"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar descripción: {str(e)}")

@app.post("/api/generative/chatbot-respuesta")
async def chatbot_respuesta(
    request: ChatbotGenerativoRequest,
    model: GenerativeModel = Depends(get_generative_model)
):
    """
    Genera una respuesta personalizada para el chatbot.
    
    *Parámetros:*
    - *pregunta*: Pregunta del usuario (requerido)
    - *contexto*: Contexto de la conversación
    
    *Retorna:*
    - Respuesta generada
    - Metadatos del proceso
    """
    try:
        resultado = model.generar_respuesta_chatbot(
            pregunta_usuario=request.pregunta,
            contexto=request.contexto,
            max_tokens=request.max_tokens
        )
        
        return {
            "success": True,
            "data": resultado,
            "message": "Respuesta generada exitosamente"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar respuesta: {str(e)}")

@app.post("/api/generative/generar-titulo-seo")
async def generar_titulo_seo(
    request: TituloSEORequest,
    model: GenerativeModel = Depends(get_generative_model)
):
    """
    Genera un título optimizado para SEO.
    
    *Parámetros:*
    - *nombre_base*: Nombre base del producto
    - *caracteristicas*: Características destacadas
    
    *Retorna:*
    - Título SEO (máximo 60 caracteres)
    """
    try:
        resultado = model.generar_titulo_producto(
            nombre_base=request.nombre_base,
            caracteristicas=request.caracteristicas
        )
        
        return {
            "success": True,
            "data": resultado,
            "message": "Título generado exitosamente"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar título: {str(e)}")

@app.post("/api/generative/generar-batch")
async def generar_batch(
    request: GenerarBatchRequest,
    model: GenerativeModel = Depends(get_generative_model)
):
    """
    Genera descripciones para múltiples productos en lote.
    
    *Parámetros:*
    - *productos*: Lista de productos con sus datos
    
    *Retorna:*
    - Lista de descripciones generadas
    """
    try:
        resultados = []
        
        for producto in request.productos:
            resultado = model.generar_descripcion_producto(
                nombre_producto=producto.get("nombre_producto", "Producto"),
                caracteristicas=producto.get("caracteristicas"),
                categoria=producto.get("categoria"),
                precio=producto.get("precio")
            )
            resultados.append(resultado)
        
        return {
            "success": True,
            "data": {
                "total_productos": len(resultados),
                "resultados": resultados
            },
            "message": f"{len(resultados)} descripciones generadas exitosamente"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en generación batch: {str(e)}")

@app.get("/api/generative/templates")
async def obtener_templates():
    """
    Obtiene la lista de templates disponibles por categoría.
    
    *Retorna:*
    - Templates disponibles
    - Categorías soportadas
    - Ejemplos de uso
    """
    if not GENERATIVE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Módulo generativo no disponible")
    
    return {
        "categorias": PromptTemplates.listar_categorias(),
        "total_templates": len(PromptTemplates.TEMPLATES),
        "ejemplo_uso": {
            "categoria": "ropa",
            "datos": {
                "nombre": "Camiseta básica",
                "caracteristicas": "Algodón suave",
                "talla": "M",
                "color": "Azul"
            }
        }
    }

@app.get("/api/generative/health")
async def generative_health_check(model: GenerativeModel = Depends(get_generative_model)):
    """
    Verifica el estado del módulo generativo.
    
    *Retorna:*
    - Estado del servicio
    - Modelo cargado
    - Timestamp actual
    """
    return {
        "status": "healthy",
        "modelo_cargado": model.default_model,
        "timestamp": datetime.now().isoformat(),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

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
    print(f"\n📖 Documentación: http://localhost:8000/docs")
    print(f"🔗 API Root: http://localhost:8000/")
    print("="*70 + "\n")

    data_dir = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print("⚠️ NOTA: Crea la carpeta 'backend/data' y coloca tus .npy, .json y .faiss ahí.")
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_excludes=[
            "*/_pycache_/*",
            "*/.",
            "*/.pyc",
            "*/data/*"
        ],
        log_level="info"
    )