"""
Módulo de IA Generativa para ComprIAssist
Generación automática de contenido usando Hugging Face

Componentes:
- GenerativeModel: Modelo principal de generación
- PromptTemplates: Templates optimizados por categoría
"""

from .generative_model import GenerativeModel, generar_descripcion_rapida
from .prompt_templates import PromptTemplates

__all__ = [
    "GenerativeModel",
    "generar_descripcion_rapida",
    "PromptTemplates"
]

__version__ = "1.0.0"
__author__ = "Equipo ComprIAssist - UPAO"