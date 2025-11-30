"""
API Endpoint para el módulo de IA Generativa
Integración con FastAPI para ComprIAssist

Autor: Equipo ComprIAssist - UPAO
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime

# Importar modelo generativo con manejo de errores
try:
    from .generative_model import GenerativeModel
    from .prompt_templates import PromptTemplates
except ImportError:
    try:
        from models.generative.generative_model import GenerativeModel
        from models.generative.prompt_templates import PromptTemplates
    except ImportError:
        from generative_model import GenerativeModel
        from prompt_templates import PromptTemplates


# Crear router
router = APIRouter(
    prefix="/api/generative",
    tags=["Generativa IA"]
)

# Instancia global del modelo (se carga una vez)
generative_model = None


def get_model():
    """Dependency para obtener instancia del modelo."""
    global generative_model
    if generative_model is None:
        generative_model = GenerativeModel()
    return generative_model


# ============================================
# MODELOS DE DATOS (Pydantic)
# ============================================

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


class ChatbotRequest(BaseModel):
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
# ENDPOINTS
# ============================================

@router.get("/")
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
            "/generar-descripcion",
            "/chatbot-respuesta",
            "/generar-titulo-seo",
            "/generar-batch",
            "/templates",
            "/health"
        ],
        "estado": "Operativo ✅"
    }


@router.post("/generar-descripcion")
async def generar_descripcion(
    request: GenerarDescripcionRequest,
    model: GenerativeModel = Depends(get_model)
):
    """
    Genera una descripción atractiva para un producto.
    
    **Parámetros:**
    - **nombre_producto**: Nombre del producto (requerido)
    - **caracteristicas**: Lista de características principales
    - **categoria**: Categoría del producto (ropa, electrónica, etc.)
    - **precio**: Precio del producto
    - **temperatura**: Nivel de creatividad (0.0-1.0)
    
    **Retorna:**
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


@router.post("/chatbot-respuesta")
async def chatbot_respuesta(
    request: ChatbotRequest,
    model: GenerativeModel = Depends(get_model)
):
    """
    Genera una respuesta personalizada para el chatbot.
    
    **Parámetros:**
    - **pregunta**: Pregunta del usuario (requerido)
    - **contexto**: Contexto de la conversación
    
    **Retorna:**
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


@router.post("/generar-titulo-seo")
async def generar_titulo_seo(
    request: TituloSEORequest,
    model: GenerativeModel = Depends(get_model)
):
    """
    Genera un título optimizado para SEO.
    
    **Parámetros:**
    - **nombre_base**: Nombre base del producto
    - **caracteristicas**: Características destacadas
    
    **Retorna:**
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


@router.post("/generar-batch")
async def generar_batch(
    request: GenerarBatchRequest,
    model: GenerativeModel = Depends(get_model)
):
    """
    Genera descripciones para múltiples productos en lote.
    
    **Parámetros:**
    - **productos**: Lista de productos con sus datos
    
    **Retorna:**
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


@router.get("/templates")
async def obtener_templates():
    """
    Obtiene la lista de templates disponibles por categoría.
    
    **Retorna:**
    - Templates disponibles
    - Categorías soportadas
    - Ejemplos de uso
    """
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


@router.get("/health")
async def health_check(model: GenerativeModel = Depends(get_model)):
    """
    Verifica el estado del módulo generativo.
    
    **Retorna:**
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
# FUNCIÓN PARA INTEGRAR CON MAIN SERVER
# ============================================

def setup_generative_routes(app):
    """
    Integra las rutas del módulo generativo con la app principal.
    
    Args:
        app: Instancia de FastAPI
    """
    app.include_router(router)
    print("✅ Rutas del módulo generativo configuradas")


if __name__ == "__main__":
    # Demo de la API
    import uvicorn
    from fastapi import FastAPI
    
    app = FastAPI(
        title="ComprIAssist - API Generativa",
        description="API de IA Generativa para descripciones de productos",
        version="1.0.0"
    )
    
    app.include_router(router)
    
    print("🚀 Iniciando servidor de desarrollo...")
    print("📖 Documentación: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)