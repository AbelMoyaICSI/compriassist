# 🚀 Guía de Inicio Rápido - ComprIAssist

## 📋 Requisitos Previos

- **Python**: 3.9 o superior
- **Node.js**: 14+ (opcional, para herramientas de frontend)
- **Navegador**: Chrome, Firefox o Edge actualizado
- **Git**: Para clonar el repositorio
- **GPU**: Recomendada para entrenar modelos de Deep Learning

## ⚡ Instalación Rápida

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/comprIAssist.git
cd comprIAssist
```

### 2. Crear Entorno Virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt

# Descargar modelos de SpaCy
python -m spacy download es_core_news_sm
python -m spacy download en_core_web_sm

# Descargar datos de NLTK
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 4. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp config/example.env config/.env

# Editar .env con tus configuraciones
# (Usar editor de texto favorito)
```

## 🌐 Ejecutar la Aplicación

### Opción 1: Solo Frontend (Demo Visual)

```bash
# Abrir directamente el archivo HTML en el navegador
start frontend/index.html  # Windows
open frontend/index.html   # Mac
xdg-open frontend/index.html  # Linux
```

**O usar un servidor local:**

```bash
# Con Python
cd frontend
python -m http.server 3000

# Luego abrir: http://localhost:3000
```

### Opción 2: Frontend + Backend (Completo)

**Terminal 1 - Backend:**
```bash
python backend/server.py
# Servidor corriendo en: http://localhost:8000
# Docs API: http://localhost:8000/docs
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python -m http.server 3000
# Frontend en: http://localhost:3000
```

## 📁 Estructura del Proyecto

```
compriassist/
│
├── frontend/               # Interfaz web
│   ├── index.html         # Página principal
│   ├── css/
│   │   └── styles.css     # Estilos con animaciones
│   └── js/
│       └── main.js        # JavaScript interactivo
│
├── backend/               # Servidor API
│   └── server.py          # FastAPI server
│
├── models/                # Módulos de IA (5 módulos)
│   ├── chatbot/
│   ├── recommendation/
│   ├── sentiment/
│   ├── visual_search/
│   └── generative/
│
├── config/                # Configuraciones
│   └── example.env
│
├── docs/                  # Documentación
│   └── ARQUITECTURA.md
│
├── requirements.txt       # Dependencias Python
├── package.json          # Metadata del proyecto
└── README.md             # Este archivo
```

## 🎯 Funcionalidades Actuales

### ✅ Implementado

1. **Frontend Completo**
   - Diseño moderno y responsive
   - Animaciones CSS avanzadas
   - Navegación suave
   - 5 secciones principales

2. **Demos Interactivas**
   - Chatbot simulado
   - Análisis de sentimientos (simulado)
   - Búsqueda visual (UI)
   - IA Generativa (UI)

3. **Backend Base**
   - API REST con FastAPI
   - Endpoints preparados para los 5 módulos
   - Documentación automática

### 🚧 En Desarrollo

1. **Modelos de IA**
   - BERT para sentimientos (entrenado, pendiente integración)
   - CNN/ResNet50 para búsqueda visual (entrenado)
   - Recomendador con ML
   - Chatbot con PLN
   - IA Generativa con T5

2. **Base de Datos**
   - Esquema diseñado
   - Pendiente implementación

## 🧪 Probar la Aplicación

### Probar Frontend

1. Abrir `frontend/index.html` en el navegador
2. Navegar por las secciones:
   - **Inicio**: Hero con estadísticas animadas
   - **Módulos IA**: Descripción de los 5 módulos
   - **Características**: 8 funcionalidades clave
   - **Demo**: Prueba interactiva de cada módulo
   - **Equipo**: Información del equipo
   - **Contacto**: Formulario de contacto

### Probar Backend API

1. Ejecutar servidor: `python backend/server.py`
2. Abrir documentación: `http://localhost:8000/docs`
3. Probar endpoints:

**Chatbot:**
```bash
curl -X POST "http://localhost:8000/api/chatbot/message" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola, busco una camiseta"}'
```

**Sentiment Analysis:**
```bash
curl -X POST "http://localhost:8000/api/sentiment/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Este producto es excelente, lo recomiendo"}'
```

## 🎨 Personalización

### Cambiar Colores

Editar variables CSS en `frontend/css/styles.css`:

```css
:root {
    --primary-color: #6366f1;     /* Color principal */
    --secondary-color: #ec4899;   /* Color secundario */
    --accent-color: #10b981;      /* Color de acento */
}
```

### Modificar Contenido

Editar `frontend/index.html` y buscar las secciones:
- Hero: línea ~50
- Módulos: línea ~150
- Características: línea ~300

## 🔧 Desarrollo

### Agregar Nuevo Endpoint

Editar `backend/server.py`:

```python
@app.post("/api/nuevo-endpoint")
async def nuevo_endpoint(data: MiModelo):
    # Tu lógica aquí
    return {"resultado": "éxito"}
```

### Agregar Nuevo Módulo de IA

1. Crear carpeta en `models/nombre_modulo/`
2. Agregar `README.md` con documentación
3. Implementar modelo en Python
4. Crear endpoint en `backend/server.py`
5. Conectar con frontend en `frontend/js/main.js`

## 📊 Siguientes Pasos

### Corto Plazo (1-2 semanas)
- [ ] Integrar modelo BERT entrenado
- [ ] Implementar sistema de recomendación básico
- [ ] Conectar búsqueda visual con ResNet50
- [ ] Base de datos con productos de ejemplo

### Mediano Plazo (1 mes)
- [ ] Chatbot funcional con NLTK
- [ ] IA Generativa con T5
- [ ] Testing completo
- [ ] Optimización de performance

### Largo Plazo (2-3 meses)
- [ ] Despliegue en producción
- [ ] Integración con base de datos real
- [ ] Monitoreo y analytics
- [ ] Documentación completa

## 🐛 Solución de Problemas

### Error: ModuleNotFoundError

```bash
# Verificar que el entorno virtual esté activado
# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: Puerto 8000 ya en uso

```bash
# Cambiar puerto en backend/server.py
# O matar proceso:
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9
```

### Frontend no carga estilos

- Verificar que las rutas en `index.html` sean correctas
- Abrir la consola del navegador (F12) para ver errores

## 📞 Soporte

Para consultas sobre el proyecto:
- **Universidad**: Universidad Privada Antenor Orrego
- **Facultad**: Ingeniería de Sistemas e IA
- **Ubicación**: Trujillo, Perú

## 📄 Licencia

Proyecto académico desarrollado para fines educativos.

---

**¡Listo para comenzar! 🎉**

Ejecuta el frontend y explora la interfaz visual con animaciones. 
Los modelos de IA se integrarán en las próximas iteraciones.
