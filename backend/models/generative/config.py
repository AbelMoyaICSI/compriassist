"""
Configuración del módulo de IA Generativa
Gestiona settings y variables de entorno

Autor: Equipo ComprIAssist - UPAO
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


class GenerativeConfig(BaseSettings):
    """Configuración del módulo generativo."""
    
    # API Keys
    HUGGINGFACE_TOKEN: Optional[str] = None
    
    # Modelos
    DEFAULT_MODEL: str = "flan-t5"
    FALLBACK_MODEL: str = "flan-t5"
    
    # Parámetros de generación por defecto
    DEFAULT_MAX_TOKENS: int = 150
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_TOP_P: float = 0.9
    
    # Límites
    MAX_TOKENS_LIMIT: int = 500
    MIN_TOKENS_LIMIT: int = 20
    MAX_BATCH_SIZE: int = 50
    
    # Timeouts (segundos)
    API_TIMEOUT: int = 30
    RETRY_ATTEMPTS: int = 3
    RETRY_DELAY: int = 2
    
    # Cache
    ENABLE_CACHE: bool = True
    CACHE_TTL: int = 3600  # 1 hora
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_REQUESTS: bool = True
    
    # Features flags
    ENABLE_BATCH_PROCESSING: bool = True
    ENABLE_FALLBACK: bool = True
    ENABLE_PROMPT_OPTIMIZATION: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Configuración global
config = GenerativeConfig()


def get_config() -> GenerativeConfig:
    """Obtiene la configuración global."""
    return config


def validar_configuracion() -> dict:
    """
    Valida la configuración actual.
    
    Returns:
        Dict con el estado de validación
    """
    errores = []
    advertencias = []
    
    # Validar token
    if not config.HUGGINGFACE_TOKEN:
        advertencias.append("⚠️ Token de HuggingFace no configurado. Funcionalidad limitada.")
    
    # Validar límites
    if config.MAX_TOKENS_LIMIT < config.MIN_TOKENS_LIMIT:
        errores.append("❌ MAX_TOKENS_LIMIT debe ser mayor que MIN_TOKENS_LIMIT")
    
    if config.DEFAULT_MAX_TOKENS > config.MAX_TOKENS_LIMIT:
        advertencias.append("⚠️ DEFAULT_MAX_TOKENS excede MAX_TOKENS_LIMIT")
    
    # Validar temperatura
    if not 0.0 <= config.DEFAULT_TEMPERATURE <= 1.0:
        errores.append("❌ DEFAULT_TEMPERATURE debe estar entre 0.0 y 1.0")
    
    return {
        "valido": len(errores) == 0,
        "errores": errores,
        "advertencias": advertencias,
        "config": {
            "token_configurado": bool(config.HUGGINGFACE_TOKEN),
            "modelo_default": config.DEFAULT_MODEL,
            "max_tokens": config.DEFAULT_MAX_TOKENS,
            "temperatura": config.DEFAULT_TEMPERATURE
        }
    }


def mostrar_configuracion():
    """Muestra la configuración actual (sin revelar secrets)."""
    print("=" * 60)
    print("CONFIGURACIÓN DEL MÓDULO GENERATIVO")
    print("=" * 60)
    
    print("\n🔑 API Keys:")
    print(f"  HuggingFace Token: {'✅ Configurado' if config.HUGGINGFACE_TOKEN else '❌ No configurado'}")
    
    print("\n🤖 Modelos:")
    print(f"  Modelo por defecto: {config.DEFAULT_MODEL}")
    print(f"  Modelo fallback: {config.FALLBACK_MODEL}")
    
    print("\n⚙️ Parámetros de generación:")
    print(f"  Max tokens: {config.DEFAULT_MAX_TOKENS}")
    print(f"  Temperatura: {config.DEFAULT_TEMPERATURE}")
    print(f"  Top-p: {config.DEFAULT_TOP_P}")
    
    print("\n🔒 Límites:")
    print(f"  Max tokens límite: {config.MAX_TOKENS_LIMIT}")
    print(f"  Min tokens límite: {config.MIN_TOKENS_LIMIT}")
    print(f"  Max batch size: {config.MAX_BATCH_SIZE}")
    
    print("\n⏱️ Timeouts:")
    print(f"  API timeout: {config.API_TIMEOUT}s")
    print(f"  Reintentos: {config.RETRY_ATTEMPTS}")
    print(f"  Delay entre reintentos: {config.RETRY_DELAY}s")
    
    print("\n💾 Cache:")
    print(f"  Habilitado: {'✅' if config.ENABLE_CACHE else '❌'}")
    print(f"  TTL: {config.CACHE_TTL}s")
    
    print("\n🎛️ Features:")
    print(f"  Batch processing: {'✅' if config.ENABLE_BATCH_PROCESSING else '❌'}")
    print(f"  Fallback: {'✅' if config.ENABLE_FALLBACK else '❌'}")
    print(f"  Optimización prompts: {'✅' if config.ENABLE_PROMPT_OPTIMIZATION else '❌'}")
    
    print("\n" + "=" * 60)
    
    # Validar
    validacion = validar_configuracion()
    
    if validacion["advertencias"]:
        print("\n⚠️ ADVERTENCIAS:")
        for adv in validacion["advertencias"]:
            print(f"  {adv}")
    
    if validacion["errores"]:
        print("\n❌ ERRORES:")
        for err in validacion["errores"]:
            print(f"  {err}")
    else:
        print("\n✅ Configuración válida")
    
    print("=" * 60)


# Configuraciones predefinidas para diferentes entornos
CONFIGS_ENTORNO = {
    "desarrollo": {
        "DEFAULT_MAX_TOKENS": 100,
        "DEFAULT_TEMPERATURE": 0.8,
        "LOG_LEVEL": "DEBUG",
        "ENABLE_CACHE": False
    },
    "produccion": {
        "DEFAULT_MAX_TOKENS": 150,
        "DEFAULT_TEMPERATURE": 0.7,
        "LOG_LEVEL": "WARNING",
        "ENABLE_CACHE": True
    },
    "testing": {
        "DEFAULT_MAX_TOKENS": 50,
        "DEFAULT_TEMPERATURE": 0.5,
        "LOG_LEVEL": "ERROR",
        "ENABLE_CACHE": False
    }
}


def aplicar_config_entorno(entorno: str):
    """
    Aplica configuración predefinida para un entorno.
    
    Args:
        entorno: 'desarrollo', 'produccion', o 'testing'
    """
    if entorno not in CONFIGS_ENTORNO:
        raise ValueError(f"Entorno '{entorno}' no válido. Opciones: {list(CONFIGS_ENTORNO.keys())}")
    
    config_env = CONFIGS_ENTORNO[entorno]
    
    for key, value in config_env.items():
        setattr(config, key, value)
    
    print(f"✅ Configuración '{entorno}' aplicada")


if __name__ == "__main__":
    # Mostrar configuración actual
    mostrar_configuracion()
    
    # Validar
    validacion = validar_configuracion()
    
    print("\n📊 RESUMEN DE VALIDACIÓN:")
    print(f"  Estado: {'✅ Válido' if validacion['valido'] else '❌ Inválido'}")
    print(f"  Errores: {len(validacion['errores'])}")
    print(f"  Advertencias: {len(validacion['advertencias'])}")
