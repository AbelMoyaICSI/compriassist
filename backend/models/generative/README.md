# Módulo 5: IA Generativa

## Descripción
Sistema de generación automática de contenido para descripciones de productos y respuestas personalizadas.

## Tecnologías
- **Modelos Transformer**:
  - T5 (Text-to-Text Transfer Transformer)
  - GPT-like models
  - BERT generativo
- **Framework**: HuggingFace Transformers, PyTorch

## Funcionalidades
1. **Generación de Descripciones de Productos**
   - Descripciones atractivas y precisas
   - Adaptadas al tono de marca
   - Optimizadas para SEO

2. **Respuestas Personalizadas en Chatbot**
   - Contextuales y coherentes
   - Adaptadas al usuario
   - Natural y conversacional

3. **Generación de Contenido Marketing**
   - Títulos llamativos
   - Bullets points
   - Comparaciones de productos

## Estructura de Archivos (Futura)
```
generative/
├── t5_generator.py            # Generador con T5
├── gpt_generator.py           # Generador con GPT
├── prompt_engineering.py      # Gestión de prompts
├── models/
│   ├── t5_finetuned/
│   └── gpt_adapted/
└── data/
    ├── product_descriptions.csv
    └── training_prompts.json
```

## Enfoques de Implementación

### Opción 1: T5 Small (Recomendado para proyecto)
- **Ventajas**: Ligero, rápido, fácil de fine-tunear
- **Tamaño**: ~60M parámetros
- **Uso**: Descripciones cortas y medianas

### Opción 2: GPT-2 Small
- **Ventajas**: Buen balance calidad/tamaño
- **Tamaño**: ~124M parámetros
- **Uso**: Respuestas conversacionales

### Opción 3: API OpenAI (Producción)
- **Ventajas**: Máxima calidad
- **Desventajas**: Costo, dependencia externa

## Métricas de Evaluación
- **BLEU Score**: Calidad de generación
- **ROUGE Score**: Similitud con referencias
- **Perplexity**: Fluidez del texto
- **Evaluación Humana**: Coherencia y utilidad

## Ejemplos de Uso

```python
# Generar descripción de producto
input: "camiseta roja, algodón, talla M"
output: "Descubre esta elegante camiseta roja confeccionada 
         en algodón 100% premium. Talla M perfecta para uso 
         diario. Combina comodidad y estilo en una sola prenda."

# Respuesta en chatbot
input: "¿Qué me recomiendas para verano?"
output: "Para el verano te recomendaría nuestra colección de 
         prendas ligeras en algodón. Tenemos camisetas frescas, 
         shorts cómodos y sandalias ideales para el clima cálido."
```

## Estado Actual
🚧 **En Desarrollo** - Estructura preparada
📋 **Pendiente**: Selección de modelo base y dataset

## Próximos Pasos
1. Seleccionar modelo base (T5-small recomendado)
2. Recopilar dataset de descripciones de calidad
3. Fine-tunear modelo con datos de e-commerce
4. Implementar prompt engineering
5. Evaluar calidad con métricas automáticas y humanas
6. Crear API para generación on-demand
7. Integrar con chatbot y módulo de productos

## Consideraciones
- **Tamaño del modelo**: Priorizar modelos pequeños para despliegue
- **Calidad vs Velocidad**: Balance entre precisión y tiempo de respuesta
- **Ética**: Evitar generación de contenido engañoso
- **Validación**: Revisión humana de descripciones generadas
