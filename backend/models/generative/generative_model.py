"""
Módulo de IA Generativa para ComprIAssist
Sistema híbrido: Intenta usar HuggingFace API, pero tiene fallback a templates inteligentes.

SOLUCIÓN GARANTIZADA - Funciona siempre

Autor: Equipo ComprIAssist - UPAO
Fecha: Noviembre 2025
"""

from typing import Optional, Dict, List
import os
from dotenv import load_dotenv
import logging
import random

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Intentar importar HuggingFace (opcional)
try:
    from huggingface_hub import InferenceClient
    HUGGINGFACE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_AVAILABLE = False
    logger.warning("⚠️ huggingface_hub no disponible. Usando solo templates.")


class GenerativeModel:
    """
    Modelo generativo híbrido:
    1. Intenta usar HuggingFace API
    2. Si falla, usa templates inteligentes (siempre funciona)
    """
    
    def __init__(self, hf_token: Optional[str] = None, use_templates_only: bool = False):
        """
        Inicializa el modelo generativo.
        
        Args:
            hf_token: Token de Hugging Face (opcional)
            use_templates_only: Si True, usa solo templates sin intentar API
        """
        self.hf_token = hf_token or os.getenv("HUGGINGFACE_TOKEN")
        self.use_templates_only = use_templates_only
        self.client = None
        
        # Intentar inicializar cliente HuggingFace
        if HUGGINGFACE_AVAILABLE and self.hf_token and not use_templates_only:
            try:
                self.client = InferenceClient(token=self.hf_token)
                logger.info("✅ Cliente HuggingFace inicializado (modo híbrido)")
            except:
                logger.warning("⚠️ No se pudo inicializar cliente HuggingFace")
                self.client = None
        
        if self.client is None or use_templates_only:
            logger.info("✅ Modo templates inteligentes activado")
        
        self.default_model = "templates"
        
        # Templates de descripciones por categoría
        self._init_templates()
    
    def _init_templates(self):
        """Inicializa templates de descripciones por categoría."""
        
        self.templates = {
            "ropa": [
                "Descubre {nombre}, confeccionado con {caracteristica1}. Perfecto para {uso}, combina {cualidad1} y {cualidad2}. {detalles}",
                "{nombre} de alta calidad con {caracteristica1}. Diseñado para {cualidad1}, ideal para tu estilo {estilo}. {detalles}",
                "Eleva tu estilo con {nombre}. Fabricado con {caracteristica1}, ofrece {cualidad1} excepcional. {detalles}",
            ],
            "electronica": [
                "{nombre} con {caracteristica1} de última generación. Equipado con {caracteristica2}, ofrece {beneficio1} y {beneficio2}. {detalles}",
                "Experimenta {nombre} con tecnología {caracteristica1}. Potencia y {cualidad1} en un solo dispositivo. {detalles}",
                "Potencia tu {uso} con {nombre}. Cuenta con {caracteristica1} y {caracteristica2} para máximo rendimiento. {detalles}",
            ],
            "deportes": [
                "{nombre} diseñado para atletas exigentes. Con {caracteristica1} y {caracteristica2}, maximiza tu {beneficio1}. {detalles}",
                "Alcanza tus metas con {nombre}. Tecnología {caracteristica1} que impulsa tu {beneficio1}. {detalles}",
                "Supera tus límites con {nombre}. {caracteristica1} avanzada para {cualidad1} superior. {detalles}",
            ],
            "hogar": [
                "Transforma tu hogar con {nombre}. Elaborado con {caracteristica1}, aporta {cualidad1} y {cualidad2} a tus espacios. {detalles}",
                "{nombre} que combina {cualidad1} y funcionalidad. Perfecto para crear ambientes {estilo}. {detalles}",
                "Dale un toque especial a tu hogar con {nombre}. {caracteristica1} de calidad premium. {detalles}",
            ],
            "belleza": [
                "{nombre} con {caracteristica1} de origen natural. Formulado para {beneficio1} y {beneficio2} visible. {detalles}",
                "Realza tu belleza con {nombre}. Enriquecido con {caracteristica1}, proporciona {cualidad1} inmediata. {detalles}",
                "Cuida tu piel con {nombre}. {caracteristica1} premium para resultados {cualidad1}. {detalles}",
            ],
            "general": [
                "Descubre {nombre}, el producto que estabas buscando. Con {caracteristica1}, ofrece {cualidad1} y {cualidad2}. {detalles}",
                "{nombre} de calidad premium. Diseñado con {caracteristica1} para tu {cualidad1} y satisfacción. {detalles}",
                "Conoce {nombre}, innovación y {cualidad1} en un solo producto. {caracteristica1} de última generación. {detalles}",
            ]
        }
        
        # Palabras para completar templates
        self.cualidades = ["comodidad", "elegancia", "estilo", "durabilidad", "calidad", "rendimiento", "confort", "versatilidad"]
        self.beneficios = ["rendimiento óptimo", "resultados excepcionales", "experiencia premium", "máxima eficiencia"]
        self.estilos = ["moderno", "clásico", "contemporáneo", "elegante", "casual", "deportivo"]
        self.usos = ["uso diario", "ocasiones especiales", "actividades deportivas", "trabajo", "entretenimiento"]
    
    def generar_descripcion_producto(
        self,
        nombre_producto: str,
        caracteristicas: Optional[List[str]] = None,
        categoria: Optional[str] = None,
        precio: Optional[float] = None,
        modelo: Optional[str] = None,
        max_tokens: int = 150,
        temperatura: float = 0.7
    ) -> Dict[str, str]:
        """
        Genera una descripción atractiva para un producto.
        Intenta usar API primero, luego templates.
        """
        
        # Intentar con HuggingFace si está disponible
        if self.client and not self.use_templates_only:
            try:
                resultado = self._generar_con_api(
                    nombre_producto, caracteristicas, categoria, precio, max_tokens, temperatura
                )
                if resultado['success']:
                    return resultado
            except Exception as e:
                logger.warning(f"⚠️ API falló, usando templates: {str(e)[:50]}")
        
        # Usar templates inteligentes (siempre funciona)
        return self._generar_con_templates(nombre_producto, caracteristicas, categoria, precio)
    
    def _generar_con_api(self, nombre: str, caracteristicas: List[str], categoria: str, 
                         precio: float, max_tokens: int, temperatura: float) -> Dict:
        """Intenta generar con API de HuggingFace."""
        
        prompt = f"Product: {nombre}\n"
        if caracteristicas:
            prompt += f"Features: {', '.join(caracteristicas[:2])}\n"
        prompt += "Description:"
        
        response = self.client.text_generation(
            prompt,
            model="distilbert/distilgpt2",
            max_new_tokens=max_tokens,
            temperature=temperatura,
            return_full_text=False
        )
        
        if response and len(response.strip()) > 10:
            return {
                "descripcion": response.strip(),
                "producto": nombre,
                "modelo_usado": "huggingface-api",
                "success": True
            }
        else:
            raise ValueError("Respuesta vacía de API")
    
    def _generar_con_templates(self, nombre: str, caracteristicas: Optional[List[str]],
                               categoria: Optional[str], precio: Optional[float]) -> Dict:
        """Genera descripción usando templates inteligentes."""
        
        # Seleccionar template según categoría
        cat = (categoria or "general").lower()
        templates_cat = self.templates.get(cat, self.templates["general"])
        template = random.choice(templates_cat)
        
        # Preparar características
        cars = caracteristicas or ["calidad premium"]
        caracteristica1 = cars[0] if len(cars) > 0 else "materiales de calidad"
        caracteristica2 = cars[1] if len(cars) > 1 else "diseño innovador"
        
        # Generar valores aleatorios pero coherentes
        cualidad1 = random.choice(self.cualidades)
        cualidad2 = random.choice([c for c in self.cualidades if c != cualidad1])
        beneficio1 = random.choice(self.beneficios)
        beneficio2 = random.choice([b for b in self.beneficios if b != beneficio1])
        estilo = random.choice(self.estilos)
        uso = random.choice(self.usos)
        
        # Agregar detalles sobre precio si existe
        detalles = ""
        if precio:
            if precio < 50:
                detalles = "Excelente relación calidad-precio."
            elif precio < 100:
                detalles = "Inversión en calidad que vale la pena."
            else:
                detalles = "Premium quality para quienes buscan lo mejor."
        
        # Completar template
        descripcion = template.format(
            nombre=nombre,
            caracteristica1=caracteristica1,
            caracteristica2=caracteristica2,
            cualidad1=cualidad1,
            cualidad2=cualidad2,
            beneficio1=beneficio1,
            beneficio2=beneficio2,
            estilo=estilo,
            uso=uso,
            detalles=detalles
        )
        
        return {
            "descripcion": descripcion,
            "producto": nombre,
            "modelo_usado": "templates-inteligentes",
            "success": True
        }
    
    def generar_respuesta_chatbot(
        self,
        pregunta_usuario: str,
        contexto: Optional[str] = None,
        modelo: Optional[str] = None,
        max_tokens: int = 200
    ) -> Dict[str, str]:
        """Genera respuesta de chatbot con análisis de intención."""
        
        pregunta_lower = pregunta_usuario.lower()
        
        # Análisis de intención
        if any(word in pregunta_lower for word in ["precio", "costo", "cuanto", "cuánto"]):
            respuesta = "Los precios de nuestros productos varían según el modelo y características. Te invito a explorar nuestro catálogo donde encontrarás opciones desde productos económicos hasta premium. ¿Te gustaría ver alguna categoría en particular?"
        
        elif any(word in pregunta_lower for word in ["envío", "envio", "entrega", "delivery"]):
            respuesta = "¡Ofrecemos envío a todo el país! El tiempo de entrega depende de tu ubicación: 2-3 días en Lima y 4-7 días a provincias. Envío gratis en compras mayores a S/100. ¿En qué distrito te encuentras?"
        
        elif any(word in pregunta_lower for word in ["devoluci", "cambio", "garantía", "garantia"]):
            respuesta = "Aceptamos devoluciones y cambios dentro de los 30 días posteriores a la compra. El producto debe estar sin usar y con su empaque original. ¿Necesitas realizar algún cambio?"
        
        elif any(word in pregunta_lower for word in ["pago", "tarjeta", "efectivo"]):
            respuesta = "Aceptamos múltiples formas de pago: tarjetas de crédito y débito, transferencias bancarias, y pago contra entrega. También trabajamos con Yape y Plin. ¿Cuál prefieres?"
        
        elif any(word in pregunta_lower for word in ["horario", "atención", "atencion"]):
            respuesta = "Nuestro horario de atención es de lunes a viernes de 9:00 AM a 6:00 PM, y sábados de 9:00 AM a 1:00 PM. ¿En qué puedo ayudarte?"
        
        elif any(word in pregunta_lower for word in ["ropa", "verano", "invierno", "temporada"]):
            respuesta = f"¡Claro! Tenemos una amplia colección de ropa {contexto.split()[-1] if contexto else 'para todas las temporadas'}. Desde prendas casuales hasta formales, con variedad de tallas y estilos. ¿Qué tipo de prenda buscas específicamente?"
        
        elif any(word in pregunta_lower for word in ["recomendar", "recomienda", "mejor", "bueno"]):
            respuesta = "Con gusto te puedo recomendar. Para darte las mejores opciones, ¿podrías decirme qué tipo de producto te interesa y cuál es tu presupuesto aproximado?"
        
        else:
            respuesta = "Estoy aquí para ayudarte con cualquier consulta sobre nuestros productos, precios, envíos, formas de pago y más. ¿Podrías darme más detalles sobre lo que necesitas?"
        
        return {
            "respuesta": respuesta,
            "pregunta": pregunta_usuario,
            "modelo_usado": "reglas-inteligentes",
            "success": True
        }
    
    def generar_titulo_producto(
        self,
        nombre_base: str,
        caracteristicas: Optional[List[str]] = None,
        modelo: Optional[str] = None
    ) -> Dict[str, str]:
        """Genera título SEO optimizado."""
        
        # Extraer palabras clave
        palabras = nombre_base.split()
        
        if caracteristicas and len(caracteristicas) > 0:
            # Tomar primeras 2 características más importantes
            cars = caracteristicas[:2]
            titulo = f"{nombre_base} - {' '.join(cars)}"
        else:
            titulo = f"{nombre_base} Premium"
        
        # Limitar a 60 caracteres
        if len(titulo) > 60:
            titulo = titulo[:57] + "..."
        
        return {
            "titulo": titulo,
            "producto": nombre_base,
            "modelo_usado": "optimizacion-seo",
            "success": True
        }


# Función helper para uso rápido
def generar_descripcion_rapida(
    nombre_producto: str,
    caracteristicas: Optional[List[str]] = None,
    hf_token: Optional[str] = None
) -> str:
    """Genera descripción rápida."""
    model = GenerativeModel(hf_token=hf_token)
    resultado = model.generar_descripcion_producto(nombre_producto, caracteristicas)
    return resultado["descripcion"]


if __name__ == "__main__":
    print("=== DEMO: Módulo Generativo ComprIAssist ===\n")
    
    generador = GenerativeModel()
    
    # Ejemplo 1: Descripción de producto
    print("1️⃣ Generando descripción de producto...")
    resultado = generador.generar_descripcion_producto(
        nombre_producto="Camiseta de algodón orgánico",
        caracteristicas=["100% algodón", "Talla M", "Color azul marino", "Eco-friendly"],
        categoria="ropa",
        precio=29.99
    )
    print(f"✅ Descripción: {resultado['descripcion']}")
    print(f"🤖 Modelo: {resultado['modelo_usado']}\n")
    
    # Ejemplo 2: Chatbot
    print("2️⃣ Generando respuesta de chatbot...")
    respuesta = generador.generar_respuesta_chatbot(
        pregunta_usuario="¿Tienen ropa para verano?",
        contexto="Usuario busca ropa casual"
    )
    print(f"🤖 Respuesta: {respuesta['respuesta']}\n")
    
    # Ejemplo 3: Título SEO
    print("3️⃣ Generando título SEO...")
    titulo = generador.generar_titulo_producto(
        nombre_base="Zapatillas deportivas Nike",
        caracteristicas=["Running", "Amortiguación Premium"]
    )
    print(f"📝 Título: {titulo['titulo']}\n")
    
    print("✅ Demo completada!")