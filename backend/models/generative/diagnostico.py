"""
Script de diagnóstico completo para HuggingFace API
"""
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
import json

load_dotenv()
token = os.getenv("HUGGINGFACE_TOKEN")

print("=" * 70)
print("DIAGNÓSTICO DE HUGGINGFACE API")
print("=" * 70)

print(f"\n✅ Token configurado: {'Sí' if token else 'No'}")
print(f"📝 Token (primeros 10 chars): {token[:10] if token else 'N/A'}")

client = InferenceClient(token=token)

# Lista de modelos a probar (varios tipos)
modelos_a_probar = [
    ("distilbert/distilgpt2", "GPT-2 Distilled"),
    ("openai-community/gpt2", "GPT-2 Base"),
    ("bigscience/bloom-560m", "BLOOM 560M"),
    ("facebook/opt-350m", "OPT 350M"),
    ("google/flan-t5-small", "FLAN-T5 Small"),
    ("microsoft/DialoGPT-small", "DialoGPT Small"),
]

print("\n" + "=" * 70)
print("PROBANDO MODELOS DE TEXT GENERATION")
print("=" * 70)

modelos_funcionando = []

for modelo_id, nombre in modelos_a_probar:
    print(f"\n🧪 Probando: {nombre} ({modelo_id})")
    print("-" * 70)
    
    try:
        # Probar con prompt simple
        response = client.text_generation(
            "Product: T-shirt\nDescription:",
            model=modelo_id,
            max_new_tokens=30,
            temperature=0.7,
            return_full_text=False
        )
        
        if response and len(response.strip()) > 0:
            print(f"✅ FUNCIONA!")
            print(f"📝 Respuesta: {response[:100]}...")
            modelos_funcionando.append((modelo_id, nombre))
        else:
            print(f"❌ Respuesta vacía")
            
    except Exception as e:
        print(f"❌ Error: {str(e)[:150]}")

print("\n" + "=" * 70)
print("PROBANDO CONVERSATIONAL API")
print("=" * 70)

# Probar con API conversacional
modelos_conversacionales = [
    "microsoft/DialoGPT-medium",
    "facebook/blenderbot-400M-distill",
]

for modelo_id in modelos_conversacionales:
    print(f"\n🧪 Probando: {modelo_id}")
    print("-" * 70)
    
    try:
        response = client.conversational(
            "Describe this product: Cotton t-shirt",
            model=modelo_id
        )
        
        print(f"✅ FUNCIONA!")
        print(f"📝 Respuesta: {response}")
        modelos_funcionando.append((modelo_id, "Conversational"))
        
    except Exception as e:
        print(f"❌ Error: {str(e)[:150]}")

print("\n" + "=" * 70)
print("RESUMEN")
print("=" * 70)

if modelos_funcionando:
    print(f"\n✅ Modelos que funcionan con tu token: {len(modelos_funcionando)}")
    for modelo_id, nombre in modelos_funcionando:
        print(f"   ✅ {nombre}: {modelo_id}")
else:
    print("\n❌ Ningún modelo funcionó con la API gratuita")
    print("\n💡 POSIBLES SOLUCIONES:")
    print("   1. Tu token puede necesitar permisos adicionales")
    print("   2. Estos modelos pueden requerir HuggingFace PRO")
    print("   3. Hay límites de rate en tu cuenta")
    print("\n🔧 ALTERNATIVAS:")
    print("   A. Usar descripciones pre-generadas con templates")
    print("   B. Usar un LLM local (como Ollama)")
    print("   C. Integrar con API de OpenAI (requiere API key)")
    print("   D. Usar modelos más simples con reglas")

print("\n" + "=" * 70)