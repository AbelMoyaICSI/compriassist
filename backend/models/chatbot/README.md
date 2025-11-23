# Módulo 1: Chatbot Conversacional

## Descripción
Este módulo implementa un chatbot conversacional inteligente que actúa como interfaz principal del asistente de compras.

## Tecnologías
- **PLN**: NLTK, SpaCy
- **Framework Web**: Streamlit
- **Backend**: Python 3.9+

## Funcionalidades
1. Detección de intenciones del usuario
2. Clasificación de consultas (buscar, comparar, reseñas, ayuda)
3. Direccionamiento a módulos específicos
4. Respuestas contextuales

## Estructura de Archivos (Futura)
```
chatbot/
├── intent_classifier.py      # Clasificador de intenciones
├── conversation_manager.py   # Gestor de conversaciones
├── nlp_processor.py          # Procesador de lenguaje natural
├── models/                   # Modelos entrenados
│   └── intent_model.pkl
└── data/
    └── training_intents.json
```

## Métricas de Evaluación
- Precisión en detección de intenciones
- Tiempo de respuesta
- Satisfacción del usuario

## Estado Actual
🚧 **En Desarrollo** - Estructura preparada, pendiente implementación de modelos

## Próximos Pasos
1. Recopilar dataset de intenciones
2. Entrenar clasificador con NLTK/SpaCy
3. Integrar con interfaz Streamlit
4. Conectar con otros módulos vía API
