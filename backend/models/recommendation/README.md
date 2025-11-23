# Módulo 2: Sistema de Recomendación

## Descripción
Sistema de recomendación de productos basado en Machine Learning supervisado y no supervisado.

## Tecnologías
- **Framework ML**: Scikit-learn
- **Algoritmos**: 
  - Regresión Logística
  - Random Forest
  - K-means (clustering)
  - KNN (K-Nearest Neighbors)

## Funcionalidades
1. Recomendaciones personalizadas basadas en historial
2. Filtrado colaborativo
3. Filtrado por contenido
4. Clustering de usuarios/productos
5. Filtros avanzados (precio, categoría, calificación)

## Estructura de Archivos (Futura)
```
recommendation/
├── collaborative_filtering.py  # Filtrado colaborativo
├── content_based.py           # Filtrado por contenido
├── hybrid_recommender.py      # Sistema híbrido
├── models/
│   ├── random_forest.pkl
│   ├── logistic_regression.pkl
│   └── kmeans_model.pkl
└── data/
    ├── user_interactions.csv
    └── product_features.csv
```

## Métricas de Evaluación
- **MAP@K** (Mean Average Precision at K)
- **NDCG** (Normalized Discounted Cumulative Gain)
- **Precision & Recall**
- **Coverage**

## Estado Actual
🚧 **En Desarrollo** - Estructura preparada, pendiente implementación

## Próximos Pasos
1. Preparar dataset de interacciones usuario-producto
2. Entrenar modelos de ML con Scikit-learn
3. Implementar sistema híbrido
4. Evaluar con métricas de recomendación
5. Crear API REST para integración
