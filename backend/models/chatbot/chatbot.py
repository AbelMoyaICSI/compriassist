"""
Módulo de Chatbot Conversacional para ComprIAssist
Utiliza API de HuggingFace para generación de respuestas naturales
"""

import os
import requests
from typing import Dict, List, Optional
from .intents import IntentClassifier

class ChatbotAssistant:
    """
    Chatbot inteligente para asistencia en compras online
    Integra clasificación de intenciones y generación de respuestas
    """
    
    def __init__(self, hf_api_key: Optional[str] = None):
        """
        Inicializa el chatbot
        
        Args:
            hf_api_key: API key de HuggingFace (opcional, usa variable de entorno)
        """
        # API Key de HuggingFace
        self.hf_api_key = hf_api_key or os.getenv("HUGGINGFACE_API_KEY")
        
        # URLs de modelos de HuggingFace
        self.hf_api_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"
        
        # Clasificador de intenciones
        self.intent_classifier = IntentClassifier()
        
        # Contexto de la tienda
        self.store_context = """
        Eres un asistente virtual experto en comercio electrónico llamado ComprIAssist.
        Trabajas en una tienda online que vende productos variados (ropa, electrónica, accesorios, etc.).
        Tu objetivo es ayudar a los clientes a encontrar productos, resolver dudas y mejorar su experiencia de compra.
        Sé amable, profesional y conciso en tus respuestas.
        """
    
    def process_message(self, message: str, user_id: Optional[str] = None) -> Dict:
        """
        Procesa un mensaje del usuario y genera una respuesta
        
        Args:
            message: Mensaje del usuario
            user_id: ID del usuario (opcional)
            
        Returns:
            Dict con respuesta, intención detectada y confianza
        """
        # 1. Clasificar intención
        intent_result = self.intent_classifier.classify(message)
        intent = intent_result['intent']
        confidence = intent_result['confidence']
        entities = intent_result['entities']
        
        # 2. Generar respuesta según la intención
        if intent == "buscar_producto":
            response = self._handle_product_search(message, entities)
        elif intent == "comparar_productos":
            response = self._handle_product_comparison(message, entities)
        elif intent == "analizar_resenas":
            response = self._handle_review_analysis(message, entities)
        elif intent == "busqueda_visual":
            response = self._handle_visual_search(message)
        elif intent == "informacion_producto":
            response = self._handle_product_info(message, entities)
        elif intent == "ayuda":
            response = self._handle_help()
        elif intent == "saludo":
            response = self._handle_greeting()
        else:
            # Para intenciones generales, usar el LLM
            response = self._generate_llm_response(message)
        
        return {
            "response": response,
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "suggestions": self._get_suggestions(intent)
        }
    
    def _generate_llm_response(self, message: str) -> str:
        """
        Genera respuesta usando HuggingFace API
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            Respuesta generada
        """
        if not self.hf_api_key:
            return self._get_fallback_response(message)
        
        try:
            headers = {"Authorization": f"Bearer {self.hf_api_key}"}
            
            prompt = f"""{self.store_context}
            
Usuario: {message}
Asistente:"""
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                self.hf_api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').strip()
                return "Lo siento, hubo un problema al generar la respuesta."
            else:
                return self._get_fallback_response(message)
                
        except Exception as e:
            print(f"Error en API de HuggingFace: {e}")
            return self._get_fallback_response(message)
    
    def _handle_product_search(self, message: str, entities: Dict) -> str:
        """Maneja búsquedas de productos"""
        product = entities.get('product', 'productos')
        return f"""¡Perfecto! Te ayudo a buscar {product}. 

🔍 Para una búsqueda más precisa, puedes:
1. Especificar características (color, marca, talla)
2. Definir tu rango de precio
3. Ver productos recomendados según tus preferencias

¿Qué características buscas en {product}?"""
    
    def _handle_product_comparison(self, message: str, entities: Dict) -> str:
        """Maneja comparaciones de productos"""
        return """📊 ¡Excelente! Te ayudo a comparar productos.

Para hacer una comparación detallada, necesito que me indiques:
• ¿Qué tipo de productos quieres comparar? (ej: celulares, laptops, zapatillas)
• ¿Tienes modelos específicos en mente?

Puedo comparar hasta 4 productos mostrando:
✓ Precio y calificaciones
✓ Características principales
✓ Análisis de reseñas
✓ Ventajas y desventajas"""
    
    def _handle_review_analysis(self, message: str, entities: Dict) -> str:
        """Maneja análisis de reseñas"""
        product = entities.get('product', 'este producto')
        return f"""💬 Análisis de reseñas para {product}

Nuestro sistema de IA puede analizar:
✓ Sentimiento general (positivo/neutral/negativo)
✓ Aspectos más mencionados
✓ Detección de reseñas sospechosas
✓ Tendencias en las opiniones

¿Quieres que analice las reseñas de algún producto en particular?"""
    
    def _handle_visual_search(self, message: str) -> str:
        """Maneja búsquedas visuales"""
        return """📸 Búsqueda Visual Activada

¡Puedes encontrar productos usando imágenes!

Cómo funciona:
1. Sube una foto del producto que te gusta
2. Nuestro sistema de IA analiza la imagen
3. Te mostramos productos similares en nuestro catálogo

¿Tienes una imagen del producto que buscas?"""
    
    def _handle_product_info(self, message: str, entities: Dict) -> str:
        """Maneja información de productos"""
        product = entities.get('product', 'productos')
        return f"""ℹ️ Información sobre {product}

Puedo proporcionarte:
• Especificaciones técnicas
• Precios actuales y ofertas
• Disponibilidad en stock
• Métodos de pago y envío
• Garantía y devoluciones

¿Qué información específica necesitas?"""
    
    def _handle_help(self) -> str:
        """Maneja solicitudes de ayuda"""
        return """🤖 ¡Hola! Soy ComprIAssist, tu asistente de compras inteligente.

Puedo ayudarte con:

🔍 **Búsqueda de productos**
   "Busco zapatillas deportivas"

📊 **Comparar opciones**
   "Compara estos dos celulares"

💬 **Analizar reseñas**
   "¿Qué opinan de este producto?"

📸 **Búsqueda por imagen**
   "Encuentra productos similares"

ℹ️ **Información general**
   "¿Cuáles son los métodos de pago?"

¿En qué puedo ayudarte hoy?"""
    
    def _handle_greeting(self) -> str:
        """Maneja saludos"""
        return """¡Hola! 👋 Bienvenido a ComprIAssist.

Soy tu asistente de compras inteligente. Estoy aquí para ayudarte a:
• Encontrar el producto perfecto
• Comparar opciones
• Analizar reseñas
• Y mucho más...

¿Qué estás buscando hoy?"""
    
    def _get_fallback_response(self, message: str) -> str:
        """Respuesta de respaldo cuando no hay API disponible"""
        return """Entiendo tu consulta. Como asistente de ComprIAssist, estoy aquí para ayudarte con:

🛍️ Búsqueda y recomendación de productos
📊 Comparación de opciones
💬 Análisis de reseñas
📸 Búsqueda visual

¿Podrías ser más específico sobre lo que necesitas? Por ejemplo:
• "Busco una laptop para diseño gráfico"
• "Compara estos dos productos"
• "Analiza las reseñas de este artículo"
"""
    
    def _get_suggestions(self, intent: str) -> List[str]:
        """
        Genera sugerencias de acciones según la intención
        
        Args:
            intent: Intención detectada
            
        Returns:
            Lista de sugerencias
        """
        suggestions_map = {
            "buscar_producto": [
                "Ver productos recomendados",
                "Filtrar por categoría",
                "Comparar opciones"
            ],
            "comparar_productos": [
                "Ver tabla comparativa",
                "Analizar reseñas",
                "Ver productos similares"
            ],
            "analizar_resenas": [
                "Ver análisis de sentimientos",
                "Detectar reseñas falsas",
                "Ver tendencias"
            ],
            "busqueda_visual": [
                "Subir imagen",
                "Ver productos similares",
                "Explorar categoría"
            ],
            "ayuda": [
                "Buscar productos",
                "Comparar opciones",
                "Ver catálogo"
            ]
        }
        
        return suggestions_map.get(intent, [
            "Buscar productos",
            "Ver recomendaciones",
            "Explorar catálogo"
        ])


# Función auxiliar para crear instancia del chatbot
def create_chatbot(hf_api_key: Optional[str] = None) -> ChatbotAssistant:
    """
    Crea una instancia del chatbot
    
    Args:
        hf_api_key: API key de HuggingFace (opcional)
        
    Returns:
        Instancia de ChatbotAssistant
    """
    return ChatbotAssistant(hf_api_key=hf_api_key)