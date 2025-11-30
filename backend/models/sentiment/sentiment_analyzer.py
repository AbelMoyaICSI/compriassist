# backend/models/sentiment/sentiment_analyzer.py
try:
    from pysentimiento import create_analyzer
    print("✅ pysentimiento importado correctamente")
    PYSENTIMIENTO_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importando pysentimiento: {e}")
    PYSENTIMIENTO_AVAILABLE = False

class SentimentModel:
    def __init__(self):
        if PYSENTIMIENTO_AVAILABLE:
            try:
                print("🔧 Intentando crear el analizador...")
                self.model = create_analyzer(task="sentiment", lang="es")
                print("✅ Analizador de sentimientos creado exitosamente")
            except Exception as e:
                print(f"❌ Error creando analizador: {e}")
                self.model = None
        else:
            print("❌ pysentimiento no disponible - usando modo respaldo")
            self.model = None

    def analyze(self, text: str):
        """
        Analiza el sentimiento usando pysentimiento (si está disponible)
        """
        if not self.model:
            print(f"🔧 Usando modo respaldo para texto: '{text}'")
            return {
                "sentiment": "neutral",
                "confidence": 0.5,
                "probabilities": {
                    "positive": 0.33,
                    "neutral": 0.34,
                    "negative": 0.33
                }
            }

        
        result = self.model.predict(text)
        
        
        return {
            "sentiment": result.output,
            "confidence": max(result.probas.values()),
            "probabilities": {
                "positive": result.probas.get("POS", 0.0),
                "neutral": result.probas.get("NEU", 0.0),
                "negative": result.probas.get("NEG", 0.0)
            }
        }