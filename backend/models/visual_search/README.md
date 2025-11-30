# Módulo 4: Búsqueda Visual de Productos

## Descripción
Sistema de búsqueda de productos por imágenes utilizando Deep Learning y embeddings visuales.

## Tecnologías
- **Framework**: TensorFlow, Keras
- **Arquitecturas**:
  - CNN 1D (clasificación)
  - ResNet50 (embeddings visuales)
- **Métricas de Similitud**: Cosine Similarity

## Funcionalidades
1. Clasificación de productos por imagen
2. Búsqueda de productos visualmente similares
3. Generación de embeddings visuales
4. Indexación eficiente para búsqueda rápida

## Resultados Actuales

### CNN 1D (Clasificación de Moda)
- **Accuracy**: 72%
- **Dataset**: Myntra Fashion (~44k imágenes)
- **Categorías**: 7 tipos de productos

### ResNet50 (Búsqueda Visual)
- **Embeddings**: 2048 dimensiones
- **Similitud**: 0.8 - 1.0 para productos muy similares
- **Velocidad**: Búsqueda en tiempo real

## Estructura de Archivos (Futura)
```
visual_search/
├── cnn_classifier.py          # Clasificador CNN
├── resnet_embeddings.py       # Generador de embeddings
├── visual_search_engine.py    # Motor de búsqueda
├── models/
│   ├── cnn_fashion.h5
│   └── resnet50_embeddings/
└── data/
    ├── product_images/
    └── embeddings.npy
```

## Dataset
- **Myntra Fashion**: 44,000 imágenes
- **Categorías**: Ropa, accesorios, calzado
- **Preprocesamiento**: Normalización L2 de embeddings

## Métricas de Evaluación
- Accuracy y Loss en clasificación
- Top-K accuracy en búsqueda
- Matriz de confusión
- Precision@K y Recall@K

## Estado Actual
✅ **CNN Entrenada** - 72% accuracy en clasificación
✅ **ResNet50** - Embeddings funcionales para búsqueda
🚧 **Optimización** - Pendiente reducción de dataset

## Próximos Pasos
1. Reducir dataset a 4-6k imágenes representativas
2. Optimizar arquitectura CNN
3. Implementar indexación con FAISS
4. Crear API para carga y búsqueda de imágenes
5. Integrar con interfaz web
