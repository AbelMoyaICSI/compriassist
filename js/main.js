/* ============================================
   COMPRIASSIST - JAVASCRIPT INTERACTIVO
   Asistente Inteligente de Compras de Productos E-commerce basado en IA
   ============================================ */

// ============================================
// CONFIGURACIÓN GLOBAL
// ============================================
const CONFIG = {
    scrollThreshold: 100,
    animationDuration: 300,
    typingSpeed: 50,
    demoResponses: {
        chatbot: [
            "Claro, puedo ayudarte a encontrar productos. ¿Qué estás buscando?",
            "Tengo acceso a nuestro catálogo completo. ¿Prefieres electrónica, ropa o accesorios?",
            "Basándome en tu búsqueda, te recomiendo estos productos...",
            "¿Te gustaría ver las reseñas de este producto?",
            "Puedo comparar hasta 4 productos para ti. ¿Cuáles te interesan?"
        ],
        sentiments: {
            positive: {
                emoji: "😊",
                label: "Positivo",
                color: "#10b981",
                confidence: 0.92
            },
            neutral: {
                emoji: "😐",
                label: "Neutral",
                color: "#6b7280",
                confidence: 0.78
            },
            negative: {
                emoji: "😞",
                label: "Negativo",
                color: "#ef4444",
                confidence: 0.86
            }
        }
    }
};

// ============================================
// UTILIDADES
// ============================================
const utils = {
    // Debounce para optimizar eventos
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

    // Detectar si un elemento está visible en viewport
    isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    },

    // Scroll suave a un elemento
    smoothScrollTo(element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    },

    // Efecto de escritura (typing effect)
    typeWriter(element, text, speed = 50) {
        let i = 0;
        element.textContent = '';
        
        return new Promise((resolve) => {
            const interval = setInterval(() => {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
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
// NAVEGACIÓN
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
        // Scroll navbar
        window.addEventListener('scroll', utils.debounce(() => this.handleScroll(), 10));
        
        // Hamburger menu
        if (this.hamburger) {
            this.hamburger.addEventListener('click', () => this.toggleMenu());
        }

        // Navigation links
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => this.handleNavClick(e));
        });

        // Cerrar menú al hacer clic fuera
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

        // Actualizar active link basado en scroll
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
            
            // Actualizar active class
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
// DEMO INTERACTIVA - TABS
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

        // Actualizar botones
        this.tabButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        // Actualizar contenido
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
// CHATBOT DEMO
// ============================================
class ChatbotDemo {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendMessage');
        this.messageCount = 0;
        
        this.init();
    }

    init() {
        if (!this.chatMessages || !this.userInput || !this.sendButton) return;

        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });
    }

    sendMessage() {
        const text = this.userInput.value.trim();
        if (!text) return;

        // Agregar mensaje del usuario
        this.addMessage(text, 'user');
        this.userInput.value = '';

        // Simular respuesta del bot
        setTimeout(() => {
            const response = this.getBotResponse();
            this.addMessage(response, 'bot');
        }, 1000);
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.innerHTML = sender === 'bot' 
            ? '<i class="fas fa-robot"></i>' 
            : '<i class="fas fa-user"></i>';

        const textDiv = document.createElement('div');
        textDiv.className = 'text';
        textDiv.textContent = text;

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(textDiv);
        this.chatMessages.appendChild(messageDiv);

        // Scroll al final
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    getBotResponse() {
        const responses = CONFIG.demoResponses.chatbot;
        const index = this.messageCount % responses.length;
        this.messageCount++;
        return responses[index];
    }
}

// ============================================
// SENTIMENT ANALYSIS DEMO
// ============================================
class SentimentDemo {
    constructor() {
        this.reviewText = document.getElementById('reviewText');
        this.analyzeButton = document.querySelector('.analyze-button');
        this.resultBox = document.getElementById('sentimentResult');
        
        this.init();
    }

    init() {
        if (!this.analyzeButton) return;

        this.analyzeButton.addEventListener('click', () => this.analyzeSentiment());
    }

    analyzeSentiment() {
        const text = this.reviewText.value.trim();
        if (!text) {
            this.showResult('Por favor, escribe una reseña para analizar', 'neutral');
            return;
        }

        // Mostrar loading
        this.showLoading();

        // Simular análisis con IA
        setTimeout(() => {
            const sentiment = this.predictSentiment(text);
            this.showResult(text, sentiment);
        }, 1500);
    }

    predictSentiment(text) {
        // Simulación simple basada en palabras clave
        const positiveWords = ['bueno', 'excelente', 'increíble', 'genial', 'perfecto', 'recomiendo', 'love', 'great'];
        const negativeWords = ['malo', 'terrible', 'pésimo', 'horrible', 'decepción', 'no recomiendo', 'bad', 'worst'];

        const lowerText = text.toLowerCase();
        let score = 0;

        positiveWords.forEach(word => {
            if (lowerText.includes(word)) score += 1;
        });

        negativeWords.forEach(word => {
            if (lowerText.includes(word)) score -= 1;
        });

        if (score > 0) return 'positive';
        if (score < 0) return 'negative';
        return 'neutral';
    }

    showLoading() {
        this.resultBox.innerHTML = `
            <div style="display: flex; align-items: center; gap: 1rem;">
                <i class="fas fa-circle-notch fa-spin" style="font-size: 2rem; color: var(--primary-color);"></i>
                <span>Analizando con BERT...</span>
            </div>
        `;
    }

    showResult(text, sentiment) {
        const config = CONFIG.demoResponses.sentiments[sentiment];
        
        this.resultBox.innerHTML = `
            <div style="text-align: center;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">${config.emoji}</div>
                <h3 style="color: ${config.color}; margin-bottom: 0.5rem; font-size: 1.5rem;">
                    Sentimiento: ${config.label}
                </h3>
                <div style="margin-bottom: 1rem;">
                    <div style="background: rgba(0,0,0,0.05); border-radius: 999px; height: 8px; overflow: hidden;">
                        <div style="background: ${config.color}; height: 100%; width: ${config.confidence * 100}%; transition: width 1s ease-out;"></div>
                    </div>
                    <p style="margin-top: 0.5rem; color: var(--text-secondary); font-size: 0.875rem;">
                        Confianza: ${(config.confidence * 100).toFixed(1)}%
                    </p>
                </div>
                <p style="color: var(--text-secondary); font-size: 0.875rem;">
                    <i class="fas fa-info-circle"></i> 
                    Análisis simulado con modelo BERT (84% accuracy en dataset real)
                </p>
            </div>
        `;
    }
}

// ============================================
// VISUAL SEARCH DEMO
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
            if (files.length > 0) {
                this.handleFile(files[0]);
            }
        });

        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                this.handleFile(e.target.files[0]);
            }
        });
    }

    handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Por favor, selecciona una imagen válida');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            this.showResults(e.target.result);
        };
        reader.readAsDataURL(file);
    }

    showResults(imageUrl) {
        // Simular productos similares
        const similarProducts = [
            { name: 'Producto Similar 1', similarity: 0.95 },
            { name: 'Producto Similar 2', similarity: 0.89 },
            { name: 'Producto Similar 3', similarity: 0.84 },
            { name: 'Producto Similar 4', similarity: 0.78 }
        ];

        this.resultsGrid.innerHTML = `
            <div style="margin-bottom: 2rem;">
                <h4 style="margin-bottom: 1rem;">Imagen Cargada:</h4>
                <img src="${imageUrl}" style="max-width: 300px; border-radius: 1rem; box-shadow: var(--shadow-lg);">
            </div>
            <div>
                <h4 style="margin-bottom: 1rem;">Productos Similares (ResNet50 + Cosine Similarity):</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;">
                    ${similarProducts.map(product => `
                        <div style="background: var(--bg-card); padding: 1rem; border-radius: 0.75rem; box-shadow: var(--shadow-sm); text-align: center;">
                            <div style="width: 100%; height: 120px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 0.5rem; margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: center; color: white;">
                                <i class="fas fa-image" style="font-size: 2rem;"></i>
                            </div>
                            <p style="font-size: 0.875rem; font-weight: 600; margin-bottom: 0.25rem;">${product.name}</p>
                            <p style="font-size: 0.75rem; color: var(--accent-color);">
                                ${(product.similarity * 100).toFixed(1)}% similar
                            </p>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
}

// ============================================
// GENERATIVE AI DEMO
// ============================================
class GenerativeDemo {
    constructor() {
        this.productName = document.getElementById('productName');
        this.productCategory = document.getElementById('productCategory');
        this.generateButton = document.querySelector('.generate-button');
        this.generatedText = document.getElementById('generatedText');
        
        this.init();
    }

    init() {
        if (!this.generateButton) return;

        this.generateButton.addEventListener('click', () => this.generateDescription());
    }

    generateDescription() {
        const name = this.productName.value.trim();
        const category = this.productCategory.value.trim();

        if (!name || !category) {
            this.generatedText.innerHTML = `
                <p style="color: var(--text-secondary);">
                    <i class="fas fa-exclamation-circle"></i>
                    Por favor, completa ambos campos
                </p>
            `;
            return;
        }

        // Mostrar loading
        this.showLoading();

        // Simular generación con T5/GPT
        setTimeout(() => {
            const description = this.generateText(name, category);
            this.showGeneratedText(description);
        }, 2000);
    }

    showLoading() {
        this.generatedText.innerHTML = `
            <div style="display: flex; align-items: center; gap: 1rem; justify-content: center;">
                <i class="fas fa-magic fa-spin" style="font-size: 2rem; color: var(--primary-color);"></i>
                <span>Generando con modelo T5...</span>
            </div>
        `;
    }

    generateText(name, category) {
        // Plantillas de descripción simuladas
        const templates = [
            `Descubre el ${name}, un producto excepcional en la categoría de ${category}. Diseñado con materiales de alta calidad y tecnología de vanguardia, este artículo combina funcionalidad y estilo. Perfecto para quienes buscan lo mejor en ${category}.`,
            
            `El ${name} redefine los estándares en ${category}. Con características innovadoras y un diseño elegante, este producto ofrece una experiencia única. Ideal para usuarios exigentes que valoran la calidad y el rendimiento.`,
            
            `Presentamos el ${name}, una solución integral en ${category}. Este producto destaca por su versatilidad, durabilidad y excelente relación calidad-precio. Una elección inteligente para tu colección de ${category}.`
        ];

        return templates[Math.floor(Math.random() * templates.length)];
    }

    showGeneratedText(text) {
        this.generatedText.innerHTML = '';
        
        const container = document.createElement('div');
        container.style.cssText = 'background: var(--bg-white); padding: 1.5rem; border-radius: 0.75rem; border: 2px solid var(--primary-color);';
        
        const icon = document.createElement('div');
        icon.innerHTML = '<i class="fas fa-check-circle" style="color: var(--accent-color); font-size: 2rem; margin-bottom: 1rem;"></i>';
        
        const textElement = document.createElement('p');
        textElement.style.cssText = 'line-height: 1.8; color: var(--text-primary); margin-bottom: 1rem;';
        
        const info = document.createElement('p');
        info.style.cssText = 'font-size: 0.875rem; color: var(--text-secondary);';
        info.innerHTML = '<i class="fas fa-info-circle"></i> Descripción generada con IA (simulación de modelo T5)';
        
        container.appendChild(icon);
        container.appendChild(textElement);
        container.appendChild(info);
        this.generatedText.appendChild(container);

        // Efecto de escritura
        utils.typeWriter(textElement, text, 30);
    }
}

// ============================================
// FORMULARIO DE CONTACTO
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
        // Simular envío
        const button = this.form.querySelector('.submit-button');
        const originalText = button.innerHTML;

        button.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Enviando...';
        button.disabled = true;

        setTimeout(() => {
            button.innerHTML = '<i class="fas fa-check"></i> ¡Mensaje Enviado!';
            button.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';

            setTimeout(() => {
                button.innerHTML = originalText;
                button.style.background = '';
                button.disabled = false;
                this.form.reset();
            }, 2000);
        }, 1500);
    }
}

// ============================================
// SCROLL TO TOP
// ============================================
class ScrollToTop {
    constructor() {
        this.button = document.getElementById('scrollTop');
        this.init();
    }

    init() {
        if (!this.button) return;

        window.addEventListener('scroll', utils.debounce(() => {
            if (window.scrollY > 500) {
                this.button.classList.add('visible');
            } else {
                this.button.classList.remove('visible');
            }
        }, 100));

        this.button.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// ============================================
// ANIMACIONES AL SCROLL
// ============================================
class ScrollAnimations {
    constructor() {
        this.elements = document.querySelectorAll('[data-aos]');
        this.init();
    }

    init() {
        // AOS ya está inicializado en el HTML
        // Aquí podemos agregar animaciones adicionales personalizadas
        
        window.addEventListener('scroll', utils.debounce(() => {
            this.checkVisibility();
        }, 50));

        this.checkVisibility();
    }

    checkVisibility() {
        // Animaciones personalizadas adicionales
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

// ============================================
// CONTADOR DE ESTADÍSTICAS
// ============================================
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
            const isPercentage = target.includes('%');
            const numericValue = parseInt(target);
            
            let current = 0;
            const increment = numericValue / 50;
            const timer = setInterval(() => {
                current += increment;
                if (current >= numericValue) {
                    stat.textContent = target;
                    clearInterval(timer);
                } else {
                    stat.textContent = Math.floor(current) + (isPercentage ? '%' : '');
                }
            }, 30);
        });
    }
}

// ============================================
// INICIALIZACIÓN
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    // Inicializar todos los componentes
    new Navigation();
    new DemoTabs();
    new ChatbotDemo();
    new SentimentDemo();
    new VisualSearchDemo();
    new GenerativeDemo();
    new ContactForm();
    new ScrollToTop();
    new ScrollAnimations();
    new StatsCounter();

    console.log('%c ComprIAssist IA ', 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-size: 20px; padding: 10px; border-radius: 5px;');
    console.log('%c Sistema de Asistente Inteligente para Productos E-commerce', 'color: #6366f1; font-size: 14px; font-weight: bold;');
    console.log('%c Universidad Privada Antenor Orrego - Trujillo, Perú', 'color: #6b7280; font-size: 12px;');
});

// Prevenir comportamientos por defecto en demos
document.addEventListener('DOMContentLoaded', () => {
    const demoInputs = document.querySelectorAll('.demo-section input, .demo-section textarea');
    demoInputs.forEach(input => {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey && e.target.tagName !== 'TEXTAREA') {
                e.preventDefault();
            }
        });
    });
});
