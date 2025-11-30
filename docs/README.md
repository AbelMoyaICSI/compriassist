# ComprIAssist - Asistente Inteligente de Compras Online

![Estado](https://img.shields.io/badge/estado-desarrollo-yellow)
![Versión](https://img.shields.io/badge/versión-1.0.0-blue)

## 📋 Descripción del Proyecto

**ComprIAssist** (Compra + IA + Assist) es un asistente inteligente de compras de **productos de e-commerce** basado en Inteligencia Artificial. Sistema completo para tiendas online que integra búsqueda de productos, recomendaciones personalizadas, análisis de reseñas y más.

Desarrollado como proyecto académico para la Universidad Privada Antenor Orrego - Trujillo, Perú.

El sistema integra **4 módulos de IA** para mejorar la experiencia de compra de **productos en tiendas online**:

1. **🤖 Chatbot Conversacional** - Consultas sobre productos vía chat inteligente
2. **💬 Análisis de Reseñas de Productos** - Clasificación de sentimientos y detección de fraudes
3. **🔍 Búsqueda Visual de Productos** - Encuentra artículos similares subiendo una foto
4. **✨ IA Generativa** - Descripciones automáticas de productos para el catálogo

---

## 🎓 Equipo de Desarrollo

**Docente:**
- Sagastegui Chigne, Teobaldo Hernán

**Integrantes:**
- Moya Acosta, Abel
- Reyes Figueroa, Brandon
- Salvador Mauricio, Luis Angel
- Solar Beltran, Joan
- Terrones Llamo, Jan
- Vilca Jimènez, Juan Carlos

---

## 🏗️ Arquitectura del Proyecto

```
comprIAssist/
│
├── frontend/                    # Interfaz de usuario (HTML/CSS/JS)
│   ├── css/                    # Estilos y animaciones
│   ├── js/                     # JavaScript interactivo
│   ├── images/                 # Imágenes del frontend
│   ├── favicon.svg             # Icono del sitio
│   └── index.html              # Página principal
│
├── backend/                     # Servidor Backend + Modelos IA
│   ├── server.py               # Servidor FastAPI principal
│   ├── requirements.txt        # Dependencias Python
│   └── models/                 # Modelos de IA (5 módulos)
│       ├── chatbot/            # Modelo de chatbot conversacional
│       ├── sentiment/          # Análisis de sentimientos + detector fraude
│       ├── visual_search/      # Búsqueda visual por imágenes
│       └── generative/         # IA generativa para descripciones
│
├── assets/                      # Recursos compartidos
│   └── icons/                  # Iconos del proyecto
│
├── config/                      # Configuraciones
│   └── example.env             # Variables de entorno
│
├── docs/                        # Documentación técnica
│
├── package.json                 # Metadatos del proyecto
├── .gitignore                   # Archivos ignorados por Git
└── README.md                    # Este archivo
```

---

## 🚀 Tecnologías Utilizadas

### Frontend
- HTML5, CSS3, JavaScript (ES6+)
- Animaciones CSS avanzadas
- Diseño responsive

### Backend
- Python 3.9+
- FastAPI / Flask
- RESTful API

### Inteligencia Artificial

**Módulo 1: Chatbot Conversacional**
- NLTK / SpaCy (procesamiento de lenguaje natural)
- Streamlit (interfaz web)

**Módulo 2: Análisis de Reseñas**
- BERT (HuggingFace Transformers)
- SVM, Naive Bayes
- Detección de anomalías para reseñas falsas

**Módulo 3: Búsqueda Visual**
- TensorFlow / Keras
- CNNs (Redes Neuronales Convolucionales)
- ResNet50 para embeddings visuales
- Cosine Similarity

**Módulo 4: IA Generativa**
- Modelos Transformer (T5, GPT-like, BERT generativo)
- Generación de texto para descripciones de productos

---

## 📊 Objetivos del Proyecto

### Objetivo General
Desarrollar un asistente inteligente de compras online que utilice técnicas de IA para mejorar la experiencia del cliente, integrando chatbot, recomendaciones personalizadas, análisis de reseñas, búsqueda visual y generación de contenido.

### Objetivos Específicos
1. Diseñar arquitectura modular con comunicación vía APIs
2. Implementar chatbot conversacional con PLN
3. Aplicar técnicas de PLN para análisis de sentimientos y detección de fraudes
4. Implementar búsqueda visual con CNNs
5. Integrar IA generativa para descripciones automáticas
6. Realizar pruebas y evaluaciones con métricas estándar

---

## 🎯 Características Principales

✅ **Interfaz conversacional** - Chat inteligente para consultas de productos  
✅ **Análisis de reseñas** - Clasificación de sentimientos (positivo/neutral/negativo)  
✅ **Detección de fraudes** - Identificación de reseñas falsas  
✅ **Búsqueda por imagen** - Encuentra productos similares con solo una foto  
✅ **Descripciones automáticas** - Generación de contenido con IA  
✅ **Comparación de productos** - Hasta 4 artículos simultáneamente  
✅ **Interfaz responsive** - Compatible con desktop y móvil  

---

## 📦 Instalación

### Requisitos Previos
- Python 3.9+
- Node.js 14+ (opcional, para herramientas de frontend)
- GPU recomendada para modelos de Deep Learning

### Pasos de Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/compriassist.git
cd compriassist

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias (cuando estén disponibles)
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp config/example.env config/.env
# Editar .env con tus configuraciones

# 5. Ejecutar el servidor (cuando esté implementado)
python backend/server.py
```

---

## 🎨 Estado Actual del Proyecto

### ✅ Completado
- [x] Estructura de carpetas profesional
- [x] Documentación inicial
- [x] Diseño de arquitectura modular

### 🚧 En Desarrollo
- [ ] Frontend con animaciones
- [ ] Integración de los 5 módulos de IA
- [ ] APIs backend
- [ ] Sistema de base de datos

### 📋 Pendiente
- [ ] Entrenamiento final de modelos
- [ ] Despliegue en producción
- [ ] Testing completo
- [ ] Documentación técnica detallada

---

## 📈 Métricas de Evaluación

Cada módulo será evaluado con métricas específicas:

- **Chatbot**: Precisión en detección de intenciones
- **Análisis de Reseñas**: Accuracy, F1-score, Precision, Recall
- **Búsqueda Visual**: Accuracy, Pérdida
- **IA Generativa**: Evaluación cualitativa

---

## 🌟 Dominio del Proyecto

**Sector:** Comercio Electrónico de Productos  
**Ubicación:** Trujillo, Perú  
**Target:** Pequeñas y medianas tiendas online de productos físicos  
**Catálogo:** Ropa, electrónica, accesorios, calzado y productos de consumo  

El sistema busca democratizar el acceso a tecnologías de IA avanzadas para pymes del sector e-commerce, permitiéndoles ofrecer experiencias de compra de productos similares a Amazon o Mercado Libre.

---

## 📄 Licencia

Este proyecto es desarrollado con fines académicos para la Universidad Privada Antenor Orrego.

---

## 📞 Contacto

Para consultas sobre el proyecto, contactar a los integrantes del equipo o al docente supervisor.

---

**Universidad Privada Antenor Orrego**  
Facultad de Ingeniería  
Programa de Estudio de Ingeniería de Sistemas e Inteligencia Artificial  
Trujillo - Perú, 2025
