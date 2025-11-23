# Arquitectura del Sistema ComprIAssist

## Visión General

ComprIAssist (Compra + IA + Assist) es un sistema modular de asistente inteligente para **tiendas de productos online** que integra 5 módulos de IA independientes pero interconectados.

**Dominio**: Catálogos de productos e-commerce (ropa, electrónica, accesorios, calzado, etc.)

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (Web UI)                        │
│                    HTML + CSS + JavaScript                      │
│                         Streamlit                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ REST API
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    BACKEND (FastAPI/Flask)                      │
│                     API Gateway & Router                        │
└──────┬────────┬────────┬────────┬────────┬──────────────────────┘
       │        │        │        │        │
       │        │        │        │        │
┌──────▼───┐ ┌─▼───┐ ┌──▼────┐ ┌─▼──────┐ ┌▼──────────┐
│ Chatbot  │ │Reco-│ │Senti- │ │Visual  │ │Generative │
│   PLN    │ │mend │ │ment   │ │Search  │ │    IA     │
│          │ │     │ │Analys.│ │        │ │           │
│  NLTK    │ │ ML  │ │ BERT  │ │  CNN   │ │    T5     │
│  SpaCy   │ │ RF  │ │ SVM   │ │ResNet50│ │   GPT     │
└──────────┘ └─────┘ └───────┘ └────────┘ └───────────┘
```

## Flujo de Datos

### 1. Consulta del Usuario
```
Usuario → Frontend → API Gateway → Chatbot (PLN)
                                      ↓
                     Detección de Intención sobre Producto
                                      ↓
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
         Recomendación Productos  Análisis       Búsqueda Visual
         del Catálogo           Reseñas         de Productos
```

### 2. Respuesta del Sistema
```
Módulos IA → API Gateway → Frontend → Usuario
              ↑
          IA Generativa (enriquece respuestas)
```

## Componentes Principales

### Frontend
- **Tecnologías**: HTML5, CSS3, JavaScript ES6+
- **Responsabilidades**:
  - Interfaz de usuario responsiva
  - Animaciones y UX
  - Comunicación con API
  - Gestión de estado local

### Backend (API Gateway)
- **Tecnologías**: FastAPI o Flask
- **Responsabilidades**:
  - Routing de requests
  - Autenticación y autorización
  - Rate limiting
  - Logging y monitoreo
  - Orquestación de módulos IA

### Módulo 1: Chatbot (PLN)
- **Input**: Texto del usuario sobre productos
- **Output**: Intención + Entidades extraídas (producto, categoría, precio, etc.)
- **Tecnologías**: NLTK, SpaCy
- **Endpoints**:
  - `POST /chatbot/message`
  - `GET /chatbot/intents`

### Módulo 2: Recomendación de Productos
- **Input**: ID usuario, contexto, preferencias, historial
- **Output**: Lista de productos del catálogo recomendados
- **Tecnologías**: Scikit-learn (RF, KNN, K-means)
- **Endpoints**:
  - `POST /recommend/products`
  - `POST /recommend/similar`

### Módulo 3: Análisis de Sentimientos (Reseñas de Productos)
- **Input**: Texto de reseña de producto
- **Output**: Sentimiento + Probabilidad + ¿Es fraude?
- **Tecnologías**: BERT, SVM, Naive Bayes
- **Endpoints**:
  - `POST /sentiment/analyze`
  - `POST /sentiment/detect-fraud`

### Módulo 4: Búsqueda Visual de Productos
- **Input**: Imagen del producto
- **Output**: Productos similares del catálogo con score de similitud
- **Tecnologías**: TensorFlow, ResNet50, CNN
- **Endpoints**:
  - `POST /visual/search`
  - `POST /visual/classify`

### Módulo 5: IA Generativa (Descripciones de Productos)
- **Input**: Contexto del producto + Tipo de generación
- **Output**: Descripción de producto para catálogo
- **Tecnologías**: T5, GPT
- **Endpoints**:
  - `POST /generate/description`
  - `POST /generate/response`

## Base de Datos

### Opción 1: Supabase (Recomendado)
```
Users
├── user_id (PK)
├── preferences (JSONB)
└── interaction_history

Products (CATÁLOGO E-COMMERCE)
├── product_id (PK)
├── name
├── description
├── category (ropa, electrónica, accesorios, etc.)
├── price
├── stock
├── brand
├── features (JSONB)
├── embeddings (Vector) -- para búsqueda visual
└── images_urls (Array)

Reviews (RESEÑAS DE PRODUCTOS)
├── review_id (PK)
├── product_id (FK)
├── user_id (FK)
├── text
├── rating (1-5 estrellas)
├── sentiment_analysis (JSONB)
└── is_fake (Boolean)

User_Product_Interactions (PARA RECOMENDACIONES)
├── interaction_id (PK)
├── user_id (FK)
├── product_id (FK)
├── interaction_type (view, click, purchase, cart)
└── timestamp
```

### Opción 2: PostgreSQL Local
- Misma estructura
- Vector extension para embeddings

## Comunicación entre Módulos

### Sincrónica (REST API)
```python
# Ejemplo: Chatbot llama a Recomendador
response = requests.post(
    'http://localhost:8000/recommend/products',
    json={'user_id': 123, 'context': 'buscar camisetas'}
)
```

### Asincrónica (Opcional - Celery + Redis)
Para tareas pesadas como reentrenamiento de modelos

## Despliegue

### Desarrollo Local
```
Frontend: http://localhost:3000
Backend: http://localhost:8000
```

### Producción (Opciones)

**Opción 1: Render/Railway**
- Frontend: Servicio estático
- Backend: Web Service (Python)
- Base de datos: Supabase

**Opción 2: Docker Compose**
```yaml
services:
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
  
  backend:
    build: ./backend
    ports: ["8000:8000"]
    depends_on:
      - db
  
  db:
    image: postgres:15
```

## Seguridad

1. **API Keys**: Variables de entorno
2. **CORS**: Configurado en backend
3. **Rate Limiting**: 100 requests/min por IP
4. **Validación**: Pydantic schemas
5. **Sanitización**: Input sanitization

## Escalabilidad

### Fase 1 (Actual)
- Monolito con módulos separados
- Base de datos única
- Sin cache

### Fase 2 (Futura)
- Microservicios independientes
- Cache con Redis
- CDN para assets estáticos
- Load balancer

## Monitoreo

- **Logs**: Python logging module
- **Métricas**: Prometheus (futuro)
- **Errores**: Sentry (futuro)
- **Performance**: Time tracking por endpoint

## Testing

```
tests/
├── unit/
│   ├── test_chatbot.py
│   ├── test_sentiment.py
│   └── ...
├── integration/
│   └── test_api_integration.py
└── e2e/
    └── test_user_flow.py
```

## Próximos Pasos de Integración

1. ✅ Estructura de carpetas
2. ✅ Frontend básico
3. ⏳ Implementar backend API
4. ⏳ Entrenar/cargar modelos IA
5. ⏳ Conectar módulos con API
6. ⏳ Testing completo
7. ⏳ Despliegue en staging
8. ⏳ Despliegue en producción
