"""
Templates de prompts para generación de descripciones por categoría.
Optimizados para obtener mejores resultados con modelos generativos.

Autor: Equipo ComprIAssist - UPAO
"""

from typing import Dict, List


class PromptTemplates:
    """
    Colección de templates de prompts optimizados para diferentes
    categorías de productos de e-commerce.
    """
    
    # Templates por categoría
    TEMPLATES = {
        "ropa": """Genera una descripción de moda atractiva para este producto:

Producto: {nombre}
Características: {caracteristicas}
Talla: {talla}
Material: {material}
Color: {color}

Descripción (estilo moderno, 2-3 oraciones, menciona estilo y comodidad):""",

        "electronica": """Genera una descripción técnica pero accesible para este producto electrónico:

Producto: {nombre}
Especificaciones: {caracteristicas}
Marca: {marca}

Descripción (profesional, menciona beneficios y tecnología, 2-3 oraciones):""",

        "hogar": """Genera una descripción acogedora para este producto de hogar:

Producto: {nombre}
Características: {caracteristicas}
Material: {material}

Descripción (cálida y práctica, 2-3 oraciones):""",

        "deportes": """Genera una descripción motivadora para este producto deportivo:

Producto: {nombre}
Características: {caracteristicas}
Uso: {uso}

Descripción (energética, menciona rendimiento y beneficios, 2-3 oraciones):""",

        "belleza": """Genera una descripción elegante para este producto de belleza:

Producto: {nombre}
Ingredientes/Características: {caracteristicas}
Beneficios: {beneficios}

Descripción (sofisticada, menciona resultados, 2-3 oraciones):""",

        "alimentos": """Genera una descripción apetitosa para este producto alimenticio:

Producto: {nombre}
Características: {caracteristicas}
Ingredientes: {ingredientes}

Descripción (deliciosa, menciona sabor y calidad, 2-3 oraciones):""",

        "juguetes": """Genera una descripción divertida para este juguete:

Producto: {nombre}
Edad recomendada: {edad}
Características: {caracteristicas}

Descripción (alegre y segura, 2-3 oraciones):""",

        "libros": """Genera una descripción intrigante para este libro:

Título: {nombre}
Autor: {autor}
Género: {genero}
Sinopsis breve: {caracteristicas}

Descripción (cautivadora, sin spoilers, 2-3 oraciones):""",
        
        "general": """Genera una descripción profesional y atractiva para este producto:

Producto: {nombre}
Características principales: {caracteristicas}

Descripción (clara y persuasiva, 2-3 oraciones):"""
    }
    
    # Templates para chatbot
    CHATBOT_TEMPLATES = {
        "bienvenida": """Eres un asistente virtual amigable de una tienda online.

Usuario dice: {mensaje}

Responde de forma cálida y profesional, ofreciendo ayuda:""",

        "recomendacion": """Eres un experto en recomendaciones de productos.

Contexto: {contexto}
Usuario pregunta: {mensaje}

Recomienda productos específicos y explica por qué:""",

        "consulta_producto": """Eres un asesor de productos experto.

Producto en cuestión: {producto}
Usuario pregunta: {mensaje}

Responde de forma clara y detallada:""",

        "queja": """Eres un representante de servicio al cliente empático.

Usuario expresa: {mensaje}

Responde con empatía, ofrece soluciones:""",
    }
    
    # Templates para marketing
    MARKETING_TEMPLATES = {
        "titulo_seo": """Genera un título SEO optimizado (máximo 60 caracteres):

Producto: {nombre}
Keywords: {keywords}

Título atractivo:""",

        "bullet_points": """Genera 3-5 puntos destacados para este producto:

Producto: {nombre}
Características: {caracteristicas}

Puntos clave (formato bullet):""",

        "comparacion": """Compara estos dos productos de forma objetiva:

Producto A: {producto_a}
Producto B: {producto_b}

Comparación (ventajas de cada uno, 2-3 oraciones):""",

        "oferta": """Genera un mensaje promocional para esta oferta:

Producto: {nombre}
Descuento: {descuento}%
Tiempo limitado: {tiempo}

Mensaje de oferta (urgente y atractivo):""",
    }
    
    @classmethod
    def obtener_template(cls, categoria: str, tipo: str = "descripcion") -> str:
        """
        Obtiene un template específico.
        
        Args:
            categoria: Categoría del producto o tipo de prompt
            tipo: Tipo de template (descripcion, chatbot, marketing)
        
        Returns:
            Template como string
        """
        if tipo == "descripcion":
            return cls.TEMPLATES.get(categoria.lower(), cls.TEMPLATES["general"])
        elif tipo == "chatbot":
            return cls.CHATBOT_TEMPLATES.get(categoria.lower(), cls.CHATBOT_TEMPLATES["bienvenida"])
        elif tipo == "marketing":
            return cls.MARKETING_TEMPLATES.get(categoria.lower())
        
        return cls.TEMPLATES["general"]
    
    @classmethod
    def listar_categorias(cls) -> List[str]:
        """Retorna lista de categorías disponibles."""
        return list(cls.TEMPLATES.keys())
    
    @classmethod
    def construir_prompt_personalizado(
        cls,
        categoria: str,
        datos: Dict[str, str]
    ) -> str:
        """
        Construye un prompt usando un template y datos específicos.
        
        Args:
            categoria: Categoría del template
            datos: Dict con los datos para llenar el template
        
        Returns:
            Prompt completo
        """
        template = cls.obtener_template(categoria)
        
        # Llenar valores faltantes con "N/A"
        datos_completos = {}
        for key in ["nombre", "caracteristicas", "marca", "material", 
                    "color", "talla", "uso", "beneficios", "ingredientes",
                    "edad", "autor", "genero"]:
            datos_completos[key] = datos.get(key, "N/A")
        
        try:
            return template.format(**datos_completos)
        except KeyError:
            # Si falta alguna key, usar template general
            return cls.TEMPLATES["general"].format(
                nombre=datos.get("nombre", "Producto"),
                caracteristicas=datos.get("caracteristicas", "Alta calidad")
            )


# Ejemplos de uso para cada categoría
EJEMPLOS_CATEGORIAS = {
    "ropa": {
        "nombre": "Camiseta de algodón orgánico",
        "caracteristicas": "Transpirable, suave, duradera",
        "talla": "M",
        "material": "100% algodón orgánico",
        "color": "Azul marino"
    },
    "electronica": {
        "nombre": "Auriculares Bluetooth Premium",
        "caracteristicas": "Cancelación de ruido, 30h batería, micrófono HD",
        "marca": "TechSound"
    },
    "deportes": {
        "nombre": "Zapatillas Running Pro",
        "caracteristicas": "Amortiguación avanzada, transpirables, ligeras",
        "uso": "Running y entrenamiento"
    },
    "belleza": {
        "nombre": "Sérum Facial Vitamina C",
        "caracteristicas": "20% Vitamina C pura, ácido hialurónico",
        "beneficios": "Ilumina, hidrata, anti-edad"
    }
}


def demo_templates():
    """Función de demostración de templates."""
    print("=== DEMO: Templates de Prompts ===\n")
    
    print("📋 Categorías disponibles:")
    for i, cat in enumerate(PromptTemplates.listar_categorias(), 1):
        print(f"  {i}. {cat.capitalize()}")
    
    print("\n" + "="*50 + "\n")
    
    # Ejemplo de cada categoría principal
    for categoria, datos in EJEMPLOS_CATEGORIAS.items():
        print(f"📦 Ejemplo: {categoria.upper()}")
        prompt = PromptTemplates.construir_prompt_personalizado(categoria, datos)
        print(prompt)
        print("\n" + "-"*50 + "\n")


if __name__ == "__main__":
    demo_templates()
