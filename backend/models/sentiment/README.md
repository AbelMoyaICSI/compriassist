# Módulo 3: Análisis de Reseñas y Sentimientos

## Descripción
Sistema dual para clasificación de sentimientos y detección de reseñas falsas.

## Tecnologías
- **Deep Learning**: BERT (HuggingFace Transformers)
- **ML Clásico**: SVM, Naive Bayes
- **Detección de Anomalías**: Isolation Forest, One-Class SVM
- **Framework**: PyTorch, Scikit-learn

## Funcionalidades
1. **Clasificación de Sentimientos**
   - Positivo
   - Neutral
   - Negativo
   
2. **Detección de Reseñas Falsas**
   - Análisis de patrones sospechosos
   - Detección de anomalías
   - Identificación de grupos colusorios

## Resultados Actuales (BERT)
- **Accuracy**: 84%
- **Precision**: 
  - Negativo: 0.76
  - Neutral: 0.80
  - Positivo: 0.97
- **Recall**:
  - Negativo: 0.75
  - Neutral: 0.89
  - Positivo: 0.88

## Estructura de Archivos (Futura)
```
sentiment/
├── bert_classifier.py         # Clasificador BERT
├── traditional_models.py      # SVM, Naive Bayes
├── fraud_detector.py          # Detector de fraudes
├── models/
│   ├── bert_sentiment/        # Modelo BERT fine-tuned
│   ├── svm_model.pkl
│   └── naive_bayes.pkl
└── data/
    ├── reviews_dataset.csv
    └── labeled_reviews.csv
```

## Dataset
- **Nombre**: E-commerce Product Ratings & Sentiments
- **Tamaño**: ~4 millones de reseñas sintéticas
- **Categorías**: 8 categorías de productos
- **Split**: 80% train, 10% validation, 10% test

## Métricas de Evaluación
- Accuracy, Precision, Recall, F1-Score
- Matriz de confusión
- ROC-AUC
- Precision-Recall Curve

## Estado Actual
✅ **BERT Entrenado** - Modelo funcional con 84% accuracy
🚧 **Detección de Fraudes** - En desarrollo

## Próximos Pasos
1. Optimizar hiperparámetros de BERT
2. Implementar detector de reseñas falsas
3. Crear API para integración
4. Desplegar modelo en producción
