# backend/models/sentiment/fraud_detector.py

import re

class FraudDetector:
    """
    Detector simple de reseñas falsas basado en patrones sospechosos.
    No es ML, pero sirve para proyecto académico.
    """

    def analyze(self, text: str) -> dict:
        suspicious_patterns = [
            r"(gratis|regalo|oferta especial)",
            r"(5 estrellas|increíble|perfecto|maravilloso){2,}",
            r"(compra ya|últimas unidades)"
        ]

        score = 0

        for pattern in suspicious_patterns:
            if re.search(pattern, text.lower()):
                score += 1

        fake_prob = min(0.1 + score * 0.25, 0.98)

        return {
            "is_fake": score > 0,
            "fake_probability": fake_prob
        }
