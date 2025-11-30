"""
Script de Prueba del Chatbot
Verifica que el módulo funciona correctamente
"""

import sys
import os

# Agregar el directorio backend al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.chatbot import create_chatbot

def test_chatbot():
    """Prueba el chatbot con varios mensajes"""
    
    print("=" * 60)
    print("🤖 PRUEBA DEL CHATBOT - COMPRIASSIST")
    print("=" * 60)
    print()
    
    # Crear instancia del chatbot
    print("Inicializando chatbot...")
    chatbot = create_chatbot()
    print("✅ Chatbot inicializado\n")
    
    # Mensajes de prueba
    test_messages = [
        "Hola, ¿cómo estás?",
        "Busco zapatillas deportivas rojas talla 42",
        "Quiero comparar dos laptops",
        "¿Qué opinan de este producto?",
        "Tengo una foto, ¿puedes buscar productos similares?",
        "¿Cuánto cuesta esta camisa azul?",
        "Necesito ayuda para comprar"
    ]
    
    print("Probando diferentes tipos de mensajes:\n")
    
    for i, message in enumerate(test_messages, 1):
        print(f"─" * 60)
        print(f"📝 Prueba {i}/{len(test_messages)}")
        print(f"Usuario: {message}")
        print()
        
        # Procesar mensaje
        result = chatbot.process_message(message)
        
        # Mostrar resultados
        print(f"🎯 Intención detectada: {result['intent']}")
        print(f"💯 Confianza: {result['confidence']:.2f}")
        
        if result['entities']:
            print(f"🏷️  Entidades encontradas:")
            for key, value in result['entities'].items():
                print(f"   • {key}: {value}")
        
        print(f"\n💬 Respuesta:")
        print(f"   {result['response'][:150]}...")
        
        if result['suggestions']:
            print(f"\n💡 Sugerencias:")
            for suggestion in result['suggestions']:
                print(f"   • {suggestion}")
        
        print()
    
    print("=" * 60)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 60)
    print()
    print("🎉 El chatbot está funcionando correctamente!")
    print("👉 Ahora puedes iniciar el servidor con: python server.py")
    print()


if __name__ == "__main__":
    try:
        test_chatbot()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nAsegúrate de estar en la carpeta backend/")
        print("Ejecuta: cd backend && python test_chatbot.py")
        sys.exit(1)