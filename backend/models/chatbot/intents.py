"""
Clasificador de Intenciones para el Chatbot
Detecta la intención del usuario usando patrones y reglas simples
"""

import re
from typing import Dict, List

class IntentClassifier:
    """
    Clasificador de intenciones basado en reglas y patrones
    """
    
    def __init__(self):
        """Inicializa el clasificador con patrones para cada intención"""
        
        # Patrones para cada intención
        self.intent_patterns = {
            "saludo": [
                r"\b(hola|hey|buenos días|buenas tardes|buenas noches|saludos|qué tal)\b",
                r"^(hi|hello)\b"
            ],
            "despedida": [
                r"\b(adiós|chao|hasta luego|nos vemos|bye|gracias|muchas gracias)\b"
            ],
            "buscar_producto": [
                r"\b(busco|buscar|quiero|necesito|estoy buscando|me interesa|quisiera)\b.*(producto|artículo|zapatos|zapatillas|camisa|pantalón|laptop|celular|audífonos|reloj)",
                r"\b(mostrar|ver|encontrar|dame|recomienda|sugerir)\b.*(productos|artículos|opciones)",
                r"\b(dónde|donde).*(encontrar|comprar|conseguir|está|están)\b",
                r"\b(tienes|tienen|hay|existe).*(disponible|en stock)\b"
            ],
            "comparar_productos": [
                r"\b(comparar|comparación|diferencia|diferencias|versus|vs)\b",
                r"\b(cuál|cual).*(mejor|recomiendas|conviene|elegir|comprar)\b",
                r"\b(entre|comparativa).*(y|o)\b",
                r"\b(pros y contras|ventajas y desventajas)\b"
            ],
            "analizar_resenas": [
                r"\b(reseña|reseñas|review|reviews|opinión|opiniones|comentario|comentarios)\b",
                r"\b(qué opinan|qué dicen|cómo califican)\b.*(producto|artículo|este)\b",
                r"\b(valoración|valoraciones|calificación|calificaciones|rating)\b",
                r"\b(bueno|malo|confiable|recomendable|vale la pena)\b"
            ],
            "busqueda_visual": [
                r"\b(foto|imagen|picture|subir imagen|buscar por imagen|similar a esta)\b",
                r"\b(parecido|similar|como este|igual a)\b.*(imagen|foto|picture)\b",
                r"\b(encuentra|busca).*(por foto|por imagen|visual)\b"
            ],
            "informacion_producto": [
                r"\b(precio|costo|cuánto cuesta|valor)\b",
                r"\b(especificaciones|características|detalles|información|info)\b",
                r"\b(talla|tallas|tamaño|tamaños|medida|medidas)\b",
                r"\b(color|colores|disponible|disponibilidad)\b",
                r"\b(material|marca|modelo|tipo)\b",
                r"\b(envío|entrega|shipping|delivery|dónde envían)\b",
                r"\b(garantía|devolución|cambio|política de devolución)\b",
                r"\b(pago|métodos de pago|formas de pago|tarjeta)\b"
            ],
            "ayuda": [
                r"\b(ayuda|ayudar|ayúdame|help|auxilio|no sé|no entiendo)\b",
                r"\b(cómo|como).*(funciona|usar|utilizar|comprar|buscar)\b",
                r"\b(qué puedes hacer|qué haces|para qué sirves)\b",
                r"\b(opciones|menú|comandos)\b"
            ]
        }
        
        # Palabras clave para extraer entidades (productos, características, etc.)
        self.product_keywords = {
            # Calzado
            "zapatillas": ["zapatillas", "tenis", "sneakers", "deportivas"],
            "zapatos": ["zapatos", "calzado"],
            "botas": ["botas", "botines"],
            # Ropa
            "camisa": ["camisa", "camisas"],
            "camiseta": ["camiseta", "polo", "polera", "remera"],
            "pantalon": ["pantalón", "pantalones", "jeans", "jean"],
            "vestido": ["vestido", "vestidos"],
            "short": ["short", "shorts", "bermuda"],
            # Electrónica
            "laptop": ["laptop", "laptops", "notebook", "portátil"],
            "celular": ["celular", "smartphone", "teléfono", "móvil", "iphone", "samsung"],
            "tablet": ["tablet", "ipad"],
            "audifonos": ["audífonos", "auriculares", "headphones", "airpods"],
            "smartwatch": ["smartwatch", "reloj inteligente", "apple watch"],
            # Accesorios
            "mochila": ["mochila", "morral"],
            "bolso": ["bolso", "cartera", "bolsa"],
            "reloj": ["reloj", "relojes"]
        }
        
        # Marcas conocidas
        self.brand_keywords = [
            "nike", "adidas", "puma", "reebok", "converse", "vans",
            "apple", "samsung", "xiaomi", "huawei", "motorola", "lg",
            "hp", "dell", "lenovo", "asus", "acer", "macbook",
            "sony", "jbl", "bose", "beats",
            "zara", "h&m", "forever 21", "gap"
        ]
        
        self.color_keywords = [
            "rojo", "roja", "rojos", "rojas",
            "azul", "azules",
            "verde", "verdes",
            "amarillo", "amarilla", "amarillos", "amarillas",
            "negro", "negra", "negros", "negras",
            "blanco", "blanca", "blancos", "blancas",
            "gris", "grises",
            "rosa", "rosado", "rosada",
            "morado", "morada", "violeta",
            "naranja", "naranjas",
            "café", "marrón",
            "beige", "crema",
            "plateado", "plata",
            "dorado", "oro"
        ]
        
        self.size_keywords = {
            "ropa": ["xs", "s", "m", "l", "xl", "xxl", "pequeño", "mediano", "grande"],
            "zapatos": ["35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45"],
            "pantallas": ["13", "14", "15", "17", "pulgadas", "\""]
        }
        
        # Características técnicas
        self.tech_specs = {
            "memoria": ["ram", "gb ram", "memoria"],
            "almacenamiento": ["gb", "tb", "ssd", "disco duro", "almacenamiento"],
            "procesador": ["intel", "amd", "ryzen", "core i3", "core i5", "core i7", "core i9"],
            "camara": ["cámara", "mp", "megapíxeles", "fotos"],
            "bateria": ["batería", "mah", "duración"]
        }
    
    def classify(self, message: str) -> Dict:
        """
        Clasifica la intención del mensaje
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            Dict con intent, confidence y entities
        """
        message_lower = message.lower().strip()
        
        # Buscar coincidencias con patrones
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    score += 1
            if score > 0:
                intent_scores[intent] = score
        
        # Determinar intención principal
        if intent_scores:
            # Obtener la intención con mayor puntaje
            main_intent = max(intent_scores, key=intent_scores.get)
            max_score = intent_scores[main_intent]
            
            # Calcular confianza (normalizada)
            total_patterns = len(self.intent_patterns[main_intent])
            confidence = min(max_score / total_patterns, 1.0)
        else:
            # Si no hay coincidencias, es consulta general
            main_intent = "general"
            confidence = 0.5
        
        # Extraer entidades
        entities = self._extract_entities(message_lower)
        
        return {
            "intent": main_intent,
            "confidence": confidence,
            "entities": entities,
            "all_intents": intent_scores
        }
    
    def _extract_entities(self, message: str) -> Dict:
        """
        Extrae entidades del mensaje (productos, colores, tallas, etc.)
        
        Args:
            message: Mensaje en minúsculas
            
        Returns:
            Dict con entidades encontradas
        """
        entities = {
            "product": None,
            "product_type": None,
            "color": None,
            "size": None,
            "brand": None,
            "price_range": None,
            "tech_specs": {}
        }
        
        # Buscar productos (ahora con categorías)
        for product_type, variations in self.product_keywords.items():
            for variation in variations:
                if variation in message:
                    entities["product"] = variation
                    entities["product_type"] = product_type
                    break
            if entities["product"]:
                break
        
        # Buscar marcas
        for brand in self.brand_keywords:
            if brand in message:
                entities["brand"] = brand
                break
        
        # Buscar colores
        for color in self.color_keywords:
            if color in message:
                entities["color"] = color
                break
        
        # Buscar tallas (contexto específico)
        if entities["product_type"] in ["camisa", "camiseta", "pantalon", "vestido", "short"]:
            for size in self.size_keywords["ropa"]:
                if f" {size} " in f" {message} " or message.endswith(f" {size}"):
                    entities["size"] = size.upper()
                    break
        elif entities["product_type"] in ["zapatillas", "zapatos", "botas"]:
            for size in self.size_keywords["zapatos"]:
                if size in message:
                    entities["size"] = size
                    break
        
        # Buscar especificaciones técnicas
        for spec_type, keywords in self.tech_specs.items():
            for keyword in keywords:
                if keyword in message:
                    # Extraer valor numérico cercano
                    pattern = rf"{keyword}\s*(\d+)"
                    match = re.search(pattern, message)
                    if match:
                        entities["tech_specs"][spec_type] = f"{match.group(1)} {keyword}"
                    else:
                        entities["tech_specs"][spec_type] = keyword
                    break
        
        # Buscar rangos de precio (mejorado)
        price_patterns = [
            r"(\d+)\s*(?:a|hasta|-|y)\s*(\d+)\s*(?:soles|dólares|usd|s/|$|s/\.|dolares)?",
            r"(?:menos de|máximo|hasta)\s*(\d+)\s*(?:soles|dólares|usd|s/|$)?",
            r"(?:más de|mínimo|desde)\s*(\d+)\s*(?:soles|dólares|usd|s/|$)?"
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, message)
            if match:
                if len(match.groups()) == 2 and match.group(2):
                    entities["price_range"] = {
                        "min": int(match.group(1)),
                        "max": int(match.group(2))
                    }
                else:
                    if "menos de" in message or "máximo" in message or "hasta" in message:
                        entities["price_range"] = {
                            "min": 0,
                            "max": int(match.group(1))
                        }
                    elif "más de" in message or "mínimo" in message or "desde" in message:
                        entities["price_range"] = {
                            "min": int(match.group(1)),
                            "max": 999999
                        }
                break
        
        # Limpiar entidades nulas
        entities = {k: v for k, v in entities.items() if v}
        if "tech_specs" in entities and not entities["tech_specs"]:
            del entities["tech_specs"]
        
        return entities
    
    def get_intent_description(self, intent: str) -> str:
        """
        Obtiene una descripción de la intención
        
        Args:
            intent: Nombre de la intención
            
        Returns:
            Descripción de la intención
        """
        descriptions = {
            "saludo": "Saludo inicial del usuario",
            "despedida": "Usuario se despide",
            "buscar_producto": "Usuario busca un producto específico",
            "comparar_productos": "Usuario quiere comparar productos",
            "analizar_resenas": "Usuario quiere ver opiniones/reseñas",
            "busqueda_visual": "Usuario quiere buscar por imagen",
            "informacion_producto": "Usuario solicita información de producto",
            "ayuda": "Usuario solicita ayuda o instrucciones",
            "general": "Consulta general"
        }
        return descriptions.get(intent, "Intención no reconocida")


# Función auxiliar para pruebas
if __name__ == "__main__":
    classifier = IntentClassifier()
    
    # Ejemplos de prueba
    test_messages = [
        "Hola, ¿cómo estás?",
        "Busco zapatillas deportivas rojas",
        "Quiero comparar estos dos celulares",
        "¿Qué opinan de este producto?",
        "Tengo una foto, ¿puedes buscar productos similares?",
        "¿Cuánto cuesta esta laptop?",
        "Ayuda, no sé cómo usar esto",
        "Necesito una camisa azul talla M"
    ]
    
    print("=== Pruebas del Clasificador de Intenciones ===\n")
    for msg in test_messages:
        result = classifier.classify(msg)
        print(f"Mensaje: '{msg}'")
        print(f"Intención: {result['intent']} (confianza: {result['confidence']:.2f})")
        print(f"Entidades: {result['entities']}")
        print("-" * 60)