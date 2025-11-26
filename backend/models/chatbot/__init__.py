"""
Módulo de Chatbot Conversacional
Detecta intenciones y genera respuestas contextuales
"""

from .chatbot import ChatbotAssistant, create_chatbot
from .intents import IntentClassifier

__all__ = ['ChatbotAssistant', 'create_chatbot', 'IntentClassifier']