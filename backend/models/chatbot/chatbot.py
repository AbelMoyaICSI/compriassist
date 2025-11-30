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
        """Maneja búsquedas de productos con respuestas específicas"""
        
        # Construir respuesta personalizada
        product = entities.get('product', 'productos')
        product_type = entities.get('product_type', 'producto')
        color = entities.get('color')
        size = entities.get('size')
        brand = entities.get('brand')
        price_range = entities.get('price_range')
        tech_specs = entities.get('tech_specs', {})
        
        # Contar cuántos detalles proporcionó el usuario
        details_count = sum([
            bool(color),
            bool(size),
            bool(brand),
            bool(price_range),
            bool(tech_specs)
        ])
        
        # Si el usuario dio MUCHOS detalles (3 o más), respuesta muy específica
        if details_count >= 3:
            response = f"🎯 **Búsqueda muy específica detectada**\n\n"
            response += f"Perfecto, entiendo exactamente lo que buscas:\n\n"
            
            response += f"📦 **Producto:** {product.capitalize()}\n"
            if brand:
                response += f"🏷️ **Marca:** {brand.upper()}\n"
            if color:
                response += f"🎨 **Color:** {color.capitalize()}\n"
            if size:
                response += f"📏 **Talla:** {size}\n"
            if price_range:
                min_p = price_range.get('min', 0)
                max_p = price_range.get('max', 999999)
                response += f"💰 **Presupuesto:** S/. {min_p} - S/. {max_p}\n"
            if tech_specs:
                response += f"⚙️ **Especificaciones:**\n"
                for spec, value in tech_specs.items():
                    response += f"   • {spec.capitalize()}: {value}\n"
            
            response += f"\n✨ **Resultados encontrados:**\n\n"
            
            # Simular resultados específicos
            if product_type in ["zapatillas", "zapatos"]:
                response += f"He encontrado **12 opciones** que coinciden con tu búsqueda:\n\n"
                response += f"🥇 **Opción 1:** {brand.upper() if brand else 'Marca'} {product.capitalize()}\n"
                response += f"   • Precio: S/. {price_range.get('min', 350) if price_range else '350'}\n"
                response += f"   • Calificación: ⭐⭐⭐⭐⭐ (4.8/5)\n"
                response += f"   • Stock: Disponible en talla {size}\n"
                response += f"   • Envío: GRATIS\n\n"
                
                response += f"🥈 **Opción 2:** {brand.upper() if brand else 'Marca'} {product.capitalize()} Pro\n"
                response += f"   • Precio: S/. {price_range.get('max', 480) if price_range else '480'}\n"
                response += f"   • Calificación: ⭐⭐⭐⭐⭐ (4.9/5)\n"
                response += f"   • Stock: Últimas unidades\n"
                response += f"   • Envío: GRATIS\n\n"
                
                response += f"🥉 **Opción 3:** {brand.upper() if brand else 'Marca'} {product.capitalize()} Elite\n"
                response += f"   • Precio: S/. {(price_range.get('min', 300) + price_range.get('max', 500))//2 if price_range else '400'}\n"
                response += f"   • Calificación: ⭐⭐⭐⭐ (4.6/5)\n"
                response += f"   • Stock: Disponible\n"
                response += f"   • Envío: GRATIS\n\n"
                
            elif product_type in ["laptop", "celular", "tablet"]:
                response += f"He encontrado **8 opciones** que coinciden:\n\n"
                response += f"🥇 **{brand.upper() if brand else 'Marca Premium'} {product.capitalize()}**\n"
                if tech_specs:
                    for spec, value in tech_specs.items():
                        response += f"   • {spec.capitalize()}: {value}\n"
                response += f"   • Precio: S/. {price_range.get('min', 2500) if price_range else '2,500'}\n"
                response += f"   • Calificación: ⭐⭐⭐⭐⭐ (4.7/5)\n"
                response += f"   • Garantía: 1 año\n\n"
                
                response += f"🥈 **{brand.upper() if brand else 'Marca'} {product.capitalize()} Plus**\n"
                response += f"   • Precio: S/. {price_range.get('max', 3500) if price_range else '3,200'}\n"
                response += f"   • Calificación: ⭐⭐⭐⭐⭐ (4.8/5)\n"
                response += f"   • Garantía: 2 años\n\n"
            
            response += f"\n💡 **Siguiente paso:**\n"
            response += f"¿Quieres ver más detalles de alguna opción? (Ej: 'Ver detalles de la opción 1')\n"
            response += f"También puedo comparar estas opciones o analizar sus reseñas."
            
            return response
        
        # Si dio algunos detalles (1-2), respuesta mediana
        elif details_count >= 1:
            # Respuesta original para cuando da algunos detalles
            if product_type in ["zapatillas", "zapatos", "botas"]:
                response = f"🔍 Perfecto, te ayudo a encontrar {product}"
                
                if brand:
                    response += f" {brand.upper()}"
                if color:
                    response += f" de color {color}"
                if size:
                    response += f" talla {size}"
                
                response += ".\n\n"
                response += "📊 Tenemos varias opciones disponibles:\n"
                response += f"• Zapatillas deportivas para running\n"
                response += f"• Zapatillas casuales urbanas\n"
                response += f"• Zapatillas de entrenamiento\n\n"
                
                if price_range:
                    min_p = price_range.get('min', 0)
                    max_p = price_range.get('max', 999999)
                    response += f"💰 Rango de precio: S/. {min_p} - S/. {max_p}\n\n"
                
                response += "¿Qué estilo prefieres? ¿Para qué actividad las usarás?"
                
            elif product_type in ["laptop", "tablet"]:
                response = f"💻 Excelente, buscas {product}"
                
                if brand:
                    response += f" marca {brand.upper()}"
                
                response += ".\n\n"
                
                if tech_specs:
                    response += "📋 Especificaciones que buscas:\n"
                    for spec, value in tech_specs.items():
                        response += f"• {spec.capitalize()}: {value}\n"
                    response += "\n"
                
                response += "Tengo estas recomendaciones:\n"
                response += f"🔹 Laptops para oficina y productividad\n"
                response += f"🔹 Laptops para diseño gráfico y edición\n"
                response += f"🔹 Laptops gaming de alto rendimiento\n\n"
                
                if price_range:
                    min_p = price_range.get('min', 0)
                    max_p = price_range.get('max', 999999)
                    response += f"💵 Presupuesto: S/. {min_p} - S/. {max_p}\n\n"
                
                response += "¿Para qué la usarás principalmente? (trabajo, gaming, diseño, estudio)"
                
            elif product_type in ["celular"]:
                response = f"📱 Genial, buscas {product}"
                
                if brand:
                    response += f" {brand.upper()}"
                if color:
                    response += f" color {color}"
                
                response += ".\n\n"
                
                if tech_specs:
                    response += "📱 Características:\n"
                    for spec, value in tech_specs.items():
                        response += f"• {spec.capitalize()}: {value}\n"
                    response += "\n"
                
                response += "Opciones disponibles:\n"
                response += f"• Gama alta (flagship)\n"
                response += f"• Gama media (mejor relación calidad-precio)\n"
                response += f"• Gama económica\n\n"
                
                if price_range:
                    min_p = price_range.get('min', 0)
                    max_p = price_range.get('max', 999999)
                    response += f"💰 Presupuesto: S/. {min_p} - S/. {max_p}\n\n"
                
                response += "¿Qué es más importante para ti? (cámara, batería, rendimiento, pantalla)"
                
            elif product_type in ["camisa", "camiseta", "pantalon", "vestido"]:
                response = f"👕 Perfecto, buscas {product}"
                
                if brand:
                    response += f" {brand.upper()}"
                if color:
                    response += f" de color {color}"
                if size:
                    response += f" talla {size}"
                
                response += ".\n\n"
                response += "Estilos disponibles:\n"
                response += f"• Casual\n"
                response += f"• Formal\n"
                response += f"• Deportivo\n\n"
                
                if price_range:
                    min_p = price_range.get('min', 0)
                    max_p = price_range.get('max', 999999)
                    response += f"💵 Rango: S/. {min_p} - S/. {max_p}\n\n"
                
                response += "¿Para qué ocasión la necesitas? (trabajo, casual, fiesta)"
                
            else:
                # Respuesta genérica mejorada
                response = f"🔍 Entendido, buscas {product}"
                
                if color:
                    response += f" de color {color}"
                if size:
                    response += f" talla {size}"
                if brand:
                    response += f" marca {brand}"
                
                response += ".\n\n"
                
                if price_range:
                    min_p = price_range.get('min', 0)
                    max_p = price_range.get('max', 999999)
                    response += f"💰 Presupuesto: S/. {min_p} - S/. {max_p}\n\n"
                
                response += "Para ayudarte mejor, ¿podrías darme más detalles sobre:\n"
                response += "• ¿Para qué lo necesitas?\n"
                response += "• ¿Alguna característica específica?\n"
                response += "• ¿Prefieres alguna marca en particular?"
            
            return response
        
        # Si NO dio detalles, respuesta muy genérica
        else:
            return f"""🔍 ¡Claro! Te ayudo a buscar {product}.

Para mostrarte las mejores opciones, necesito saber:
• ¿Qué marca prefieres?
• ¿Qué color te gusta?
• ¿Cuál es tu presupuesto?
• ¿Talla o tamaño?

Ejemplo: "Busco {product} Nike rojas talla 42 entre 200 y 400 soles"

¿Qué características buscas?"""
    
    def _handle_product_comparison(self, message: str, entities: Dict) -> str:
        """Maneja comparaciones de productos"""
        product = entities.get('product', 'productos')
        product_type = entities.get('product_type')
        
        if product_type in ["laptop", "celular", "tablet"]:
            return f"""📊 Perfecto, te ayudo a comparar {product}.

Nuestro sistema puede comparar hasta 4 productos mostrándote:

**Especificaciones Técnicas:**
✓ Procesador y rendimiento
✓ Memoria RAM y almacenamiento
✓ Calidad de pantalla
✓ Duración de batería
✓ Cámara y multimedia

**Análisis de Reseñas:**
✓ Opiniones de usuarios verificados
✓ Puntos fuertes y débiles
✓ Calificación promedio

**Precio y Valor:**
✓ Comparativa de precios
✓ Relación calidad-precio
✓ Ofertas disponibles

¿Qué modelos específicos quieres comparar? (Ej: "iPhone 15 vs Samsung S24")"""
        
        elif product_type in ["zapatillas", "zapatos"]:
            return f"""📊 Excelente, compararé {product} para ti.

Te mostraré una comparativa con:

**Características:**
✓ Material y durabilidad
✓ Comodidad y amortiguación
✓ Diseño y estilo
✓ Peso y flexibilidad

**Opiniones:**
✓ Calificación de usuarios
✓ Comentarios sobre calidad
✓ Recomendaciones de talla

**Precio:**
✓ Rango de precios
✓ Ofertas actuales
✓ Relación calidad-precio

¿Qué modelos o marcas quieres comparar?"""
        
        else:
            return f"""📊 ¡Claro! Te ayudo a comparar {product}.

Puedo comparar hasta 4 artículos mostrándote:
• Características principales
• Precio y ofertas disponibles
• Calificaciones de usuarios
• Análisis de reseñas (positivas vs negativas)
• Relación calidad-precio

¿Qué productos específicos quieres comparar? Dame los nombres o modelos."""
    
    def _handle_review_analysis(self, message: str, entities: Dict) -> str:
        """Maneja análisis de reseñas"""
        product = entities.get('product', 'este producto')
        brand = entities.get('brand')
        
        response = f"💬 **Análisis de Reseñas**"
        
        if brand:
            response += f" - {brand.upper()}"
        
        response += f"\n\n"
        response += f"Voy a analizar las opiniones sobre {product}.\n\n"
        response += f"**Mi sistema de IA puede detectar:**\n\n"
        response += f"📊 **Análisis de Sentimiento:**\n"
        response += f"• Porcentaje de opiniones positivas/negativas\n"
        response += f"• Tendencia general del producto\n"
        response += f"• Calificación promedio\n\n"
        response += f"🔍 **Aspectos Más Mencionados:**\n"
        response += f"• Calidad del producto\n"
        response += f"• Relación precio-calidad\n"
        response += f"• Durabilidad\n"
        response += f"• Atención al cliente\n\n"
        response += f"⚠️ **Detección de Reseñas Falsas:**\n"
        response += f"• Identificación de comentarios sospechosos\n"
        response += f"• Verificación de usuarios\n"
        response += f"• Patrones de fraude\n\n"
        
        if brand and brand.lower() in ["apple", "samsung", "nike", "adidas"]:
            response += f"**Dato Interesante:** {brand.upper()} suele tener buenas calificaciones en nuestra plataforma.\n\n"
        
        response += f"¿Quieres que analice las reseñas de algún producto específico? Dame el nombre o modelo."
        
        return response
    
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
        product_type = entities.get('product_type')
        brand = entities.get('brand')
        
        response = f"ℹ️ **Información"
        if brand:
            response += f" - {brand.upper()}"
        response += f"**\n\n"
        
        # Información específica según tipo de producto
        if product_type in ["laptop", "celular", "tablet"]:
            response += f"📱💻 Para {product}, te puedo proporcionar:\n\n"
            response += f"**Especificaciones Técnicas:**\n"
            response += f"• Procesador y rendimiento\n"
            response += f"• Memoria RAM y almacenamiento\n"
            response += f"• Pantalla y resolución\n"
            response += f"• Batería y autonomía\n"
            response += f"• Sistema operativo\n\n"
            response += f"**Información Comercial:**\n"
            response += f"• Precio actual y ofertas\n"
            response += f"• Disponibilidad en stock\n"
            response += f"• Colores disponibles\n"
            response += f"• Garantía del fabricante\n\n"
            response += f"**Compra:**\n"
            response += f"• Métodos de pago (tarjeta, PayPal, contra entrega)\n"
            response += f"• Envío gratis en compras mayores a S/. 100\n"
            response += f"• Devoluciones hasta 30 días\n"
            
        elif product_type in ["zapatillas", "zapatos", "botas"]:
            response += f"👟 Para {product}, te puedo mostrar:\n\n"
            response += f"**Detalles del Producto:**\n"
            response += f"• Tallas disponibles (34-45)\n"
            response += f"• Colores en stock\n"
            response += f"• Material y tecnología\n"
            response += f"• Tipo de suela\n\n"
            response += f"**Precios y Ofertas:**\n"
            response += f"• Precio regular\n"
            response += f"• Descuentos activos\n"
            response += f"• Promociones por temporada\n\n"
            response += f"**Guía de Tallas:**\n"
            response += f"• Equivalencias internacionales\n"
            response += f"• Recomendaciones de ajuste\n"
            response += f"• Opiniones sobre tallaje\n\n"
            response += f"**Envío y Devoluciones:**\n"
            response += f"• Envío express 24-48h\n"
            response += f"• Cambios de talla sin costo\n"
            response += f"• Garantía de calidad\n"
            
        elif product_type in ["camisa", "camiseta", "pantalon", "vestido"]:
            response += f"👕 Sobre {product}:\n\n"
            response += f"**Información de Tallas:**\n"
            response += f"• Tallas disponibles: XS, S, M, L, XL, XXL\n"
            response += f"• Guía de medidas\n"
            response += f"• Recomendaciones de ajuste\n\n"
            response += f"**Detalles:**\n"
            response += f"• Material y composición\n"
            response += f"• Colores disponibles\n"
            response += f"• Instrucciones de cuidado\n"
            response += f"• País de fabricación\n\n"
            response += f"**Compra:**\n"
            response += f"• Precio y promociones\n"
            response += f"• Stock por talla y color\n"
            response += f"• Envío y devoluciones\n"
            
        else:
            response += f"Puedo proporcionarte:\n\n"
            response += f"• **Especificaciones** técnicas detalladas\n"
            response += f"• **Precios** actuales y ofertas especiales\n"
            response += f"• **Disponibilidad** en stock\n"
            response += f"• **Métodos de pago** (tarjeta, PayPal, transferencia)\n"
            response += f"• **Envío** a todo el país\n"
            response += f"• **Garantía** y política de devoluciones\n\n"
        
        response += f"\n¿Qué información específica necesitas sobre {product}?"
        
        return response
    
    def _handle_help(self) -> str:
        """Maneja solicitudes de ayuda"""
        return """🤖 **Guía de Uso - ComprIAssist**

Aquí están todas las formas en que puedo ayudarte:

---

**🔍 BUSCAR PRODUCTOS**
Ejemplos:
• "Busco zapatillas Nike rojas talla 42"
• "Necesito una laptop HP para diseño"
• "Quiero un celular Samsung entre 1000 y 2000 soles"
• "Muéstrame camisas azules talla L"

**📊 COMPARAR PRODUCTOS**
Ejemplos:
• "Compara iPhone 15 vs Samsung Galaxy S24"
• "Diferencias entre estas dos laptops"
• "Cuál es mejor: Nike Air Max o Adidas Ultraboost"

**💬 ANALIZAR RESEÑAS**
Ejemplos:
• "¿Qué opinan de las zapatillas Adidas?"
• "Analiza las reseñas de este celular"
• "¿Es confiable esta marca?"
• "¿Tiene buenas calificaciones?"

**📸 BÚSQUEDA VISUAL**
Ejemplos:
• "Tengo una foto de unas zapatillas similares"
• "Busca productos parecidos a esta imagen"
• "Encuentra algo como esto"

**ℹ️ INFORMACIÓN DE PRODUCTOS**
Ejemplos:
• "¿Cuánto cuesta el iPhone 15?"
• "¿Tienen stock en talla M?"
• "¿Cuáles son los métodos de pago?"
• "¿Hacen envíos a provincia?"

---

**💡 CONSEJOS:**
• Sé específico: menciona marca, color, talla, precio
• Usa ejemplos: "Como las Nike Air Jordan"
• Pregunta directo: "¿Cuánto cuesta?" es mejor que "Precio"

¿En qué puedo ayudarte ahora?"""
    
    def _handle_greeting(self) -> str:
        """Maneja saludos"""
        return """¡Hola! 👋 Bienvenido a **ComprIAssist**.

Soy tu asistente inteligente de compras. Puedo ayudarte con:

🛍️ **Búsqueda de Productos**
   "Busco zapatillas Nike rojas talla 42"
   "Necesito una laptop para diseño gráfico"

📊 **Comparar Opciones**
   "Compara iPhone 15 vs Samsung S24"
   "Diferencias entre estas zapatillas"

💬 **Analizar Reseñas**
   "¿Qué opinan de este producto?"
   "¿Es confiable esta marca?"

📸 **Búsqueda Visual**
   "Tengo una foto de un producto similar"

💰 **Información de Productos**
   "¿Cuánto cuesta esta laptop?"
   "¿Tienen disponible en talla M?"

¿Qué producto estás buscando hoy?"""
    
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