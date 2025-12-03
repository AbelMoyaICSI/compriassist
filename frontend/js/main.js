/* ============================================
   COMPRIASSIST - JAVASCRIPT INTERACTIVO
   Asistente Inteligente de Compras de Productos E-commerce basado en IA
   ============================================ */

// ============================================
// CONFIGURACIÓN GLOBAL
// ============================================
const CONFIG = {
    // URL de tu Backend FastAPI
    API_BASE_URL: "http://localhost:8000", 
    scrollThreshold: 100,
    animationDuration: 300,
    typingSpeed: 50,
    // (Hemos eliminado demoResponses.chatbot porque ya usaremos IA real)
    demoResponses: {
        sentiments: {
            positive: { emoji: "😊", label: "Positivo", color: "#10b981", confidence: 0.92 },
            neutral: { emoji: "😐", label: "Neutral", color: "#6b7280", confidence: 0.78 },
            negative: { emoji: "😞", label: "Negativo", color: "#ef4444", confidence: 0.86 }
        }
    }
};

// ============================================
// UTILIDADES (Sin cambios)
// ============================================
const utils = {
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    },
    smoothScrollTo(element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    },
    typeWriter(element, text, speed = 50) {
        let i = 0;
        element.innerHTML = ''; // Cambiado a innerHTML para permitir etiquetas HTML si es necesario
        return new Promise((resolve) => {
            const interval = setInterval(() => {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                } else {
                    clearInterval(interval);
                    resolve();
                }
            }, speed);
        });
    }
};

// ============================================
// NAVEGACIÓN (Sin cambios)
// ============================================
class Navigation {
    constructor() {
        this.navbar = document.getElementById('navbar');
        this.navMenu = document.getElementById('navMenu');
        this.hamburger = document.getElementById('hamburger');
        this.navLinks = document.querySelectorAll('.nav-link');
        this.init();
    }
    init() {
        window.addEventListener('scroll', utils.debounce(() => this.handleScroll(), 10));
        if (this.hamburger) {
            this.hamburger.addEventListener('click', () => this.toggleMenu());
        }
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => this.handleNavClick(e));
        });
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.navbar')) {
                this.closeMenu();
            }
        });
    }
    handleScroll() {
        if (window.scrollY > CONFIG.scrollThreshold) {
            this.navbar.classList.add('scrolled');
        } else {
            this.navbar.classList.remove('scrolled');
        }
        this.updateActiveLink();
    }
    toggleMenu() {
        this.navMenu.classList.toggle('active');
        this.hamburger.classList.toggle('active');
    }
    closeMenu() {
        this.navMenu.classList.remove('active');
        this.hamburger.classList.remove('active');
    }
    handleNavClick(e) {
        e.preventDefault();
        const targetId = e.target.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        if (targetSection) {
            utils.smoothScrollTo(targetSection);
            this.closeMenu();
            this.navLinks.forEach(link => link.classList.remove('active'));
            e.target.classList.add('active');
        }
    }
    updateActiveLink() {
        const sections = document.querySelectorAll('section[id]');
        const scrollY = window.scrollY;
        sections.forEach(section => {
            const sectionHeight = section.offsetHeight;
            const sectionTop = section.offsetTop - 100;
            const sectionId = section.getAttribute('id');
            const navLink = document.querySelector(`.nav-link[href="#${sectionId}"]`);
            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                this.navLinks.forEach(link => link.classList.remove('active'));
                if (navLink) navLink.classList.add('active');
            }
        });
    }
}

// ============================================
// DEMO INTERACTIVA - TABS (Sin cambios)
// ============================================
class DemoTabs {
    constructor() {
        this.tabButtons = document.querySelectorAll('.tab-button');
        this.tabPanes = document.querySelectorAll('.tab-pane');
        this.init();
    }
    init() {
        this.tabButtons.forEach(button => {
            button.addEventListener('click', () => this.switchTab(button));
        });
    }
    switchTab(button) {
        const targetTab = button.getAttribute('data-tab');
        this.tabButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        this.tabPanes.forEach(pane => {
            if (pane.id === targetTab) {
                pane.classList.add('active');
            } else {
                pane.classList.remove('active');
            }
        });
    }
}

// ============================================
// CHATBOT FLOTANTE REAL (CONECTADO AL BACKEND)
// ============================================
class FloatingChatbot {
    constructor() {
        // IDs específicos para el Widget Flotante
        this.widget = document.getElementById('chatWidget');
        this.toggleBtn = document.getElementById('chatToggleBtn');
        this.closeBtn = document.getElementById('closeChatBtn');
        this.messagesArea = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.suggestionsArea = document.getElementById('suggestionsArea');
        
        this.isOpen = false;
        this.init();
    }

    init() {
        if (!this.toggleBtn || !this.widget) return;

        // Toggle del widget
        this.toggleBtn.addEventListener('click', () => this.toggleChat());
        if(this.closeBtn) this.closeBtn.addEventListener('click', () => this.toggleChat());

        // Enviar mensajes
        if(this.sendBtn) this.sendBtn.addEventListener('click', () => this.sendMessage());
        if(this.userInput) {
            this.userInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') this.sendMessage();
            });
        }
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        if (this.isOpen) {
            this.widget.classList.add('active');
            setTimeout(() => this.userInput.focus(), 300);
        } else {
            this.widget.classList.remove('active');
        }
    }

    async sendMessage(text = null) {
        const message = text || this.userInput.value.trim();
        if (!message) return;

        // 1. Mostrar mensaje usuario
        this.addMessage(message, 'user');
        this.userInput.value = '';
        if(this.suggestionsArea) this.suggestionsArea.innerHTML = '';

        // 2. Mostrar indicador de carga
        const loadingId = this.showLoading();

        try {
            // 3. Petición al Backend
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/chatbot/message`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    message: message,
                    user_id: "invitado_web" 
                })
            });

            if (!response.ok) throw new Error('Error en conexión');
            const data = await response.json();

            // 4. Procesar respuesta
            this.removeLoading(loadingId);
            
            // Reemplazar saltos de línea por <br>
            const formattedResponse = data.response.replace(/\n/g, '<br>');
            this.addMessage(formattedResponse, 'bot');

            // 5. Renderizar sugerencias
            if (data.suggestions && data.suggestions.length > 0) {
                this.renderSuggestions(data.suggestions);
            }

        } catch (error) {
            this.removeLoading(loadingId);
            this.addMessage("Lo siento, no puedo conectarme con el servidor. Verifica que 'server.py' esté corriendo.", 'bot');
            console.error(error);
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        // Estructura interna para estilo
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = text; // innerHTML para soportar <br> y <b>

        messageDiv.appendChild(contentDiv);
        this.messagesArea.appendChild(messageDiv);
        this.messagesArea.scrollTop = this.messagesArea.scrollHeight;
    }

    showLoading() {
        const id = 'loading-' + Date.now();
        const div = document.createElement('div');
        div.id = id;
        div.className = 'message bot-message';
        div.innerHTML = '<div class="message-content">...</div>';
        this.messagesArea.appendChild(div);
        this.messagesArea.scrollTop = this.messagesArea.scrollHeight;
        return id;
    }

    removeLoading(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    renderSuggestions(suggestions) {
        if(!this.suggestionsArea) return;
        
        suggestions.forEach(sug => {
            const chip = document.createElement('button');
            chip.className = 'suggestion-chip';
            chip.textContent = sug;
            chip.onclick = () => this.sendMessage(sug);
            this.suggestionsArea.appendChild(chip);
        });
    }
}

// ============================================
// SENTIMENT ANALYSIS DEMO (CONECTADO AL BACKEND)
// ============================================
class SentimentDemo {
    constructor() {
        this.reviewText = document.getElementById('reviewText');
        // Usamos el ID específico que acabamos de poner en el HTML
        this.analyzeButton = document.getElementById('btnAnalyzeSentiment'); 
        this.resultBox = document.getElementById('sentimentResult');
        this.init();
    }

    init() {
        if (!this.analyzeButton) {
            console.error("Botón de análisis de sentimiento no encontrado");
            return;
        }
        
        this.analyzeButton.addEventListener('click', () => this.analyzeSentiment());
    }

    async analyzeSentiment() {
        const text = this.reviewText.value.trim();
        
        if (!text) {
            alert("Por favor, escribe una reseña para analizar.");
            this.reviewText.focus();
            return;
        }

        // 1. Mostrar estado de carga
        const originalBtnText = this.analyzeButton.innerHTML;
        this.analyzeButton.disabled = true;
        this.analyzeButton.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Analizando...';
        
        this.resultBox.style.display = 'block';
        this.showLoading();

        try {
            // 2. Petición al Backend
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/sentiment/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) {
                throw new Error("Error en el servidor");
            }

            const data = await response.json();

            // 3. Mostrar Resultados Reales
            this.showResult(data);

        } catch (error) {
            console.error("Error Sentiment AI:", error);
            this.resultBox.innerHTML = `
                <div style="color: #ef4444; padding: 1rem; background: #fef2f2; border-radius: 0.5rem; text-align: center;">
                    <i class="fas fa-exclamation-circle"></i> Error de conexión con el servidor.
                </div>
            `;
        } finally {
            // Restaurar botón
            this.analyzeButton.disabled = false;
            this.analyzeButton.innerHTML = originalBtnText;
        }
    }

    showLoading() {
        this.resultBox.innerHTML = `
            <div style="display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 2rem;">
                <i class="fas fa-brain fa-pulse" style="font-size: 2.5rem; color: var(--primary-color);"></i>
                <span style="color: var(--text-secondary);">Analizando emociones y detectando veracidad...</span>
            </div>
        `;
    }

    showResult(data) {
        // 1. Mapa de estilos robusto (acepta POS/positive, NEG/negative, etc.)
        const styleMap = {
            'POS': { label: 'Positivo', icon: 'fa-smile', color: '#10b981', class: 'fill-pos' },
            'positive': { label: 'Positivo', icon: 'fa-smile', color: '#10b981', class: 'fill-pos' },
            'NEU': { label: 'Neutral', icon: 'fa-meh', color: '#f59e0b', class: 'fill-neu' },
            'neutral': { label: 'Neutral', icon: 'fa-meh', color: '#f59e0b', class: 'fill-neu' },
            'NEG': { label: 'Negativo', icon: 'fa-frown', color: '#ef4444', class: 'fill-neg' },
            'negative': { label: 'Negativo', icon: 'fa-frown', color: '#ef4444', class: 'fill-neg' }
        };

        // 2. Obtener estilo según el sentimiento (usando fallback si no coincide)
        const sentimentKey = data.sentiment; 
        const sentimentInfo = styleMap[sentimentKey] || styleMap['neutral'];
        
        const isFake = data.is_fake;
        
        // 3. Construir HTML
        let html = `
            <div class="sentiment-card">
                <div class="sentiment-header">
                    <i class="fas ${sentimentInfo.icon} sentiment-icon" style="color: ${sentimentInfo.color}"></i>
                    <div>
                        <h3 style="color: ${sentimentInfo.color}; margin: 0;">${sentimentInfo.label}</h3>
                        <small style="color: #6b7280;">Confianza: ${(data.confidence * 100).toFixed(1)}%</small>
                    </div>
                </div>
        `;

        // Alerta de Fraude
        if (isFake) {
            html += `
                <div class="fraud-alert">
                    <i class="fas fa-exclamation-triangle"></i>
                    <div class="fraud-content">
                        <strong>Posible Reseña Falsa Detectada</strong>
                        <p>Nuestro modelo ha detectado patrones inusuales. Probabilidad de fraude: ${(data.fake_probability * 100).toFixed(1)}%</p>
                    </div>
                </div>
            `;
        }

        // Barras de probabilidad
        html += `<div class="probability-bars">`;
        
        // Iteramos las probabilidades del backend
        for (const [key, val] of Object.entries(data.probabilities)) {
            // key puede ser "positive", "neutral" o "negative"
            // Ahora styleMap lo encontrará correctamente
            const style = styleMap[key] || styleMap['neutral'];
            const percentage = (val * 100).toFixed(1);
            
            html += `
                <div class="bar-row">
                    <span class="bar-label">${style.label}</span>
                    <div class="bar-track">
                        <div class="bar-fill ${style.class}" style="width: ${percentage}%"></div>
                    </div>
                    <span class="bar-percent">${percentage}%</span>
                </div>
            `;
        }

        html += `</div></div>`; // Cerrar card

        this.resultBox.innerHTML = html;
    }
}
// ============================================
// VISUAL SEARCH DEMO (Sin cambios)
// ============================================
class VisualSearchDemo {
    constructor() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('imageUpload');
        this.resultsGrid = document.getElementById('visualResults');
        this.init();
    }
    init() {
        if (!this.uploadArea) return;
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.style.borderColor = 'var(--primary-color)';
            this.uploadArea.style.background = 'rgba(99, 102, 241, 0.05)';
        });
        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.style.borderColor = '';
            this.uploadArea.style.background = '';
        });
        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.style.borderColor = '';
            this.uploadArea.style.background = '';
            const files = e.dataTransfer.files;
            if (files.length > 0) this.handleFile(files[0]);
        });
        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) this.handleFile(e.target.files[0]);
        });
    }
    handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Por favor, selecciona una imagen válida');
            return;
        }
        const reader = new FileReader();
        reader.onload = (e) => { this.showPreviewAndLoading(e.target.result); };
        reader.readAsDataURL(file);
        this.uploadToBackend(file);
    }
    showPreviewAndLoading(imageUrl) {
        this.resultsGrid.innerHTML = `
            <div style="margin-bottom: 2rem;">
                <h4 style="margin-bottom: 1rem;">Imagen Cargada:</h4>
                <img src="${imageUrl}" style="max-width: 300px; border-radius: 1rem; box-shadow: var(--shadow-lg);">
            </div>
            <div>
                <h4 style="margin-bottom: 1rem;">Buscando productos similares...</h4>
                <div style="display: flex; align-items: center; justify-content: center; padding: 2rem;">
                    <i class="fas fa-circle-notch fa-spin" style="font-size: 2rem; color: var(--primary-color); margin-right: 10px;"></i>
                    <span>Procesando embeddings con ResNet50...</span>
                </div>
            </div>
        `;
    }
    async uploadToBackend(file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('top_k', 4);
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/visual/search`, {
                method: 'POST',
                body: formData
            });
            if (!response.ok) throw new Error(`Error: ${response.status}`);
            const data = await response.json();
            this.renderResults(data.similar_products);
        } catch (error) {
            console.error("Error en búsqueda visual:", error);
            const loadingDiv = this.resultsGrid.lastElementChild;
            loadingDiv.innerHTML = `<h4 style="color: #ef4444;">Error de conexión con el servidor.</h4>`;
        }
    }
    renderResults(products) {
        const resultsContainer = this.resultsGrid.lastElementChild;
        if (!products || products.length === 0) {
            resultsContainer.innerHTML = `<p>No se encontraron productos similares.</p>`;
            return;
        }
        let productsHTML = `
            <h4 style="margin-bottom: 1rem;">Resultados Similares:</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1.5rem;">
        `;
        products.map(product => {
            const similarityPercent = (product.similarity * 100).toFixed(1);
            const imgUrl = product.image_url || 'https://via.placeholder.com/200?text=Sin+Imagen';
            productsHTML += `
                <div class="product-card" style="background: var(--bg-card); border-radius: 0.75rem; box-shadow: var(--shadow-sm); overflow: hidden; transition: transform 0.3s ease;">
                    <div style="position: relative; height: 160px; overflow: hidden;">
                        <img src="${imgUrl}" alt="${product.name}" style="width: 100%; height: 100%; object-fit: cover;">
                        <span style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;">${similarityPercent}%</span>
                    </div>
                    <div style="padding: 1rem;">
                        <h5 style="font-size: 0.95rem; margin-bottom: 0.5rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${product.name}</h5>
                        <div style="display: flex; justify-content: space-between;">
                            <span style="font-size: 0.8rem; color: var(--text-secondary);">${product.category || 'General'}</span>
                            ${product.price ? `<span style="font-weight: bold; color: var(--primary-color);">$${product.price}</span>` : ''}
                        </div>
                    </div>
                </div>
            `;
        });
        productsHTML += `</div>`;
        resultsContainer.innerHTML = productsHTML;
    }
}

// ============================================
// GENERATIVE AI DEMO (INTEGRADO CON BACKEND)
// ============================================
class GenerativeDemo {
    constructor() {
        this.productName = document.getElementById('productName');
        this.productCategory = document.getElementById('productCategory');
        this.productFeatures = document.getElementById('productFeatures'); // Nuevo campo
        this.productPrice = document.getElementById('productPrice');       // Nuevo campo
        
        this.generateButton = document.getElementById('btnGenerar');
        this.resultContainer = document.getElementById('generatedResultContainer');
        this.generatedText = document.getElementById('generatedText');
        this.modelBadge = document.getElementById('modelUsedName');

        this.init();
    }

    init() {
        if (!this.generateButton) return;
        this.generateButton.addEventListener('click', () => this.generateDescription());
    }

    async generateDescription() {
        // 1. Obtener valores
        const name = this.productName.value.trim();
        const category = this.productCategory.value.trim();
        const price = parseFloat(this.productPrice.value) || 0;
        
        // Convertir características de string (coma separated) a array
        const featuresInput = this.productFeatures.value;
        const features = featuresInput 
            ? featuresInput.split(',').map(s => s.trim()).filter(s => s !== "") 
            : [];

        // Validación simple
        if (!name) {
            alert("Por favor, ingresa al menos el nombre del producto.");
            this.productName.focus();
            return;
        }

        // 2. Mostrar estado de carga
        const originalBtnText = this.generateButton.innerHTML;
        this.generateButton.disabled = true;
        this.generateButton.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Generando...';
        
        this.resultContainer.style.display = 'block';
        this.showLoading();

        try {
            // 3. Petición al Backend
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/generative/generar-descripcion`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    nombre_producto: name,
                    caracteristicas: features,
                    categoria: category || "general",
                    precio: price,
                    temperatura: 0.7
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Error en el servidor");
            }

            const data = await response.json();

            // 4. Mostrar Resultados
            if (data.success) {
                this.showGeneratedText(data.data.descripcion);
                
                // Mostrar qué modelo se usó (HuggingFace API o Templates)
                const modelo = data.data.modelo_usado || "IA Generativa";
                this.modelBadge.textContent = `Generado con: ${modelo}`;
                if (modelo.includes("templates")) {
                    this.modelBadge.style.color = "#d97706"; // Ambar si es template
                } else {
                    this.modelBadge.style.color = "#10b981"; // Verde si es API real
                }
            } else {
                this.generatedText.innerHTML = `<p style="color: red;">Error: No se pudo generar la descripción.</p>`;
            }

        } catch (error) {
            console.error("Error Generative AI:", error);
            this.generatedText.innerHTML = `
                <div style="color: #ef4444; padding: 1rem; background: #fef2f2; border-radius: 0.5rem;">
                    <strong>Error:</strong> No se pudo conectar con el módulo generativo. 
                    <br><small>Verifica que el backend esté corriendo en ${CONFIG.API_BASE_URL}</small>
                </div>
            `;
        } finally {
            // Restaurar botón
            this.generateButton.disabled = false;
            this.generateButton.innerHTML = originalBtnText;
        }
    }

    showLoading() {
        this.generatedText.innerHTML = `
            <div style="display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 2rem;">
                <i class="fas fa-brain fa-pulse" style="font-size: 2.5rem; color: var(--primary-color);"></i>
                <span style="color: var(--text-secondary);">La IA está redactando la descripción...</span>
            </div>
        `;
        this.modelBadge.textContent = "Procesando...";
    }

    showGeneratedText(text) {
        this.generatedText.innerHTML = '';
        
        const container = document.createElement('div');
        container.style.cssText = 'background: #ffffff; padding: 1.5rem; border-radius: 0.75rem; border-left: 4px solid var(--primary-color); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);';
        
        const textElement = document.createElement('p');
        textElement.style.cssText = 'line-height: 1.8; color: var(--text-primary); font-size: 1.05rem;';
        
        container.appendChild(textElement);
        this.generatedText.appendChild(container);

        // Efecto de escritura
        utils.typeWriter(textElement, text, 20);
    }
}

// ============================================
// OTROS COMPONENTES (Formulario, Scroll, Stats) - Sin cambios significativos
// ============================================
class ContactForm {
    constructor() {
        this.form = document.getElementById('contactForm');
        this.init();
    }
    init() {
        if (!this.form) return;
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });
    }
    handleSubmit() {
        const button = this.form.querySelector('.submit-button');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Enviando...';
        setTimeout(() => {
            button.innerHTML = '<i class="fas fa-check"></i> ¡Mensaje Enviado!';
            setTimeout(() => { button.innerHTML = originalText; this.form.reset(); }, 2000);
        }, 1500);
    }
}

class ScrollToTop {
    constructor() {
        this.button = document.getElementById('scrollTop');
        this.init();
    }
    init() {
        if (!this.button) return;
        window.addEventListener('scroll', utils.debounce(() => {
            if (window.scrollY > 500) this.button.classList.add('visible');
            else this.button.classList.remove('visible');
        }, 100));
        this.button.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
}

class ScrollAnimations {
    constructor() {
        this.elements = document.querySelectorAll('[data-aos]');
        this.init();
    }
    init() {
        window.addEventListener('scroll', utils.debounce(() => this.checkVisibility(), 50));
        this.checkVisibility();
    }
    checkVisibility() {
        const moduleCards = document.querySelectorAll('.module-card');
        moduleCards.forEach((card, index) => {
            if (utils.isInViewport(card)) {
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 100);
            }
        });
    }
}

class StatsCounter {
    constructor() {
        this.stats = document.querySelectorAll('.stat-number');
        this.animated = false;
        this.init();
    }
    init() {
        window.addEventListener('scroll', () => {
            if (!this.animated && this.isStatsVisible()) {
                this.animateStats();
                this.animated = true;
            }
        });
    }
    isStatsVisible() {
        const heroStats = document.querySelector('.hero-stats');
        return heroStats && utils.isInViewport(heroStats);
    }
    animateStats() {
        this.stats.forEach(stat => {
            const target = stat.textContent;
            const numericValue = parseInt(target);
            let current = 0;
            const increment = numericValue / 50;
            const timer = setInterval(() => {
                current += increment;
                if (current >= numericValue) {
                    stat.textContent = target;
                    clearInterval(timer);
                } else {
                    stat.textContent = Math.floor(current) + (target.includes('%') ? '%' : '');
                }
            }, 30);
        });
    }
}

// ============================================
// INICIALIZACIÓN
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    new Navigation();
    new DemoTabs();
    // REEMPLAZO: Usamos el FloatingChatbot en lugar del ChatbotDemo
    new FloatingChatbot(); 
    new SentimentDemo();
    new VisualSearchDemo();
    new GenerativeDemo();
    new ContactForm();
    new ScrollToTop();
    new ScrollAnimations();
    new StatsCounter();

    console.log('%c ComprIAssist IA ', 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-size: 20px;');
    console.log('%c Backend conectado en: ' + CONFIG.API_BASE_URL, 'color: #10b981; font-weight: bold;');
});