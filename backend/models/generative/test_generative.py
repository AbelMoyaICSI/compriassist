"""
Script de prueba completo para el módulo de IA Generativa
Ejemplos de uso para todas las funcionalidades

Autor: Equipo ComprIAssist - UPAO
Fecha: Noviembre 2025
"""

import sys
import os

# Agregar path del backend si es necesario
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from generative_model import GenerativeModel
from prompt_templates import PromptTemplates, EJEMPLOS_CATEGORIAS
from config import mostrar_configuracion, validar_configuracion

import time


def separador(titulo="", char="="):
    """Imprime un separador visual."""
    print(f"\n{char * 70}")
    if titulo:
        print(f"{titulo.center(70)}")
        print(char * 70)
    print()


def test_configuracion():
    """Prueba 1: Verificar configuración."""
    separador("PRUEBA 1: CONFIGURACIÓN", "=")
    
    print("📋 Mostrando configuración actual...")
    mostrar_configuracion()
    
    print("\n🔍 Validando configuración...")
    validacion = validar_configuracion()
    
    if validacion["valido"]:
        print("✅ Configuración válida y lista para usar")
    else:
        print("❌ Hay problemas en la configuración:")
        for error in validacion["errores"]:
            print(f"  {error}")
    
    return validacion["valido"]


def test_modelo_basico():
    """Prueba 2: Inicialización del modelo."""
    separador("PRUEBA 2: INICIALIZACIÓN DEL MODELO", "=")
    
    try:
        print("🔄 Inicializando modelo generativo...")
        modelo = GenerativeModel()
        print(f"✅ Modelo inicializado correctamente")
        print(f"   Modelo por defecto: {modelo.default_model}")
        print(f"   Token configurado: {'Sí ✅' if modelo.hf_token else 'No ❌'}")
        return modelo
    except Exception as e:
        print(f"❌ Error al inicializar modelo: {str(e)}")
        return None


def test_descripcion_producto(modelo):
    """Prueba 3: Generación de descripción de producto."""
    separador("PRUEBA 3: DESCRIPCIÓN DE PRODUCTO", "=")
    
    productos_ejemplo = [
        {
            "nombre": "Camiseta de algodón orgánico",
            "caracteristicas": ["100% algodón", "Talla M", "Color azul", "Eco-friendly"],
            "categoria": "ropa",
            "precio": 29.99
        },
        {
            "nombre": "Auriculares Bluetooth Premium",
            "caracteristicas": ["Cancelación de ruido", "30h batería", "Bluetooth 5.0"],
            "categoria": "electronica",
            "precio": 79.99
        },
        {
            "nombre": "Zapatillas Running Pro",
            "caracteristicas": ["Amortiguación avanzada", "Transpirables", "Ligeras"],
            "categoria": "deportes",
            "precio": 89.99
        }
    ]
    
    resultados_exitosos = 0
    
    for i, producto in enumerate(productos_ejemplo, 1):
        print(f"\n📦 Producto {i}: {producto['nombre']}")
        print(f"   Categoría: {producto['categoria']}")
        print(f"   Precio: ${producto['precio']}")
        print(f"   Características: {', '.join(producto['caracteristicas'])}")
        
        print(f"\n🔄 Generando descripción...")
        inicio = time.time()
        
        resultado = modelo.generar_descripcion_producto(
            nombre_producto=producto['nombre'],
            caracteristicas=producto['caracteristicas'],
            categoria=producto['categoria'],
            precio=producto['precio']
        )
        
        tiempo = time.time() - inicio
        
        if resultado['success']:
            print(f"✅ Descripción generada en {tiempo:.2f}s:")
            print(f"\n   📝 {resultado['descripcion']}")
            print(f"\n   🤖 Modelo usado: {resultado['modelo_usado']}")
            resultados_exitosos += 1
        else:
            print(f"❌ Error: {resultado.get('error', 'Desconocido')}")
        
        print("-" * 70)
    
    print(f"\n📊 RESUMEN: {resultados_exitosos}/{len(productos_ejemplo)} descripciones generadas exitosamente")
    return resultados_exitosos == len(productos_ejemplo)


def test_chatbot(modelo):
    """Prueba 4: Respuestas de chatbot."""
    separador("PRUEBA 4: RESPUESTAS DE CHATBOT", "=")
    
    preguntas_ejemplo = [
        {
            "pregunta": "¿Tienen ropa para verano?",
            "contexto": "Usuario busca ropa casual"
        },
        {
            "pregunta": "¿Cuál es la mejor zapatilla para correr?",
            "contexto": "Usuario es corredor principiante"
        },
        {
            "pregunta": "¿Aceptan devoluciones?",
            "contexto": "Usuario tiene dudas sobre política de devoluciones"
        }
    ]
    
    resultados_exitosos = 0
    
    for i, item in enumerate(preguntas_ejemplo, 1):
        print(f"\n💬 Pregunta {i}: {item['pregunta']}")
        print(f"   Contexto: {item['contexto']}")
        
        print(f"\n🔄 Generando respuesta...")
        inicio = time.time()
        
        resultado = modelo.generar_respuesta_chatbot(
            pregunta_usuario=item['pregunta'],
            contexto=item['contexto']
        )
        
        tiempo = time.time() - inicio
        
        if resultado['success']:
            print(f"✅ Respuesta generada en {tiempo:.2f}s:")
            print(f"\n   🤖 {resultado['respuesta']}")
            resultados_exitosos += 1
        else:
            print(f"❌ Error: {resultado.get('error', 'Desconocido')}")
        
        print("-" * 70)
    
    print(f"\n📊 RESUMEN: {resultados_exitosos}/{len(preguntas_ejemplo)} respuestas generadas exitosamente")
    return resultados_exitosos == len(preguntas_ejemplo)


def test_titulo_seo(modelo):
    """Prueba 5: Generación de títulos SEO."""
    separador("PRUEBA 5: TÍTULOS SEO", "=")
    
    productos_ejemplo = [
        {
            "nombre": "Zapatillas deportivas Nike",
            "caracteristicas": ["Running", "Amortiguación", "Transpirables"]
        },
        {
            "nombre": "Laptop gaming",
            "caracteristicas": ["RTX 4060", "16GB RAM", "144Hz"]
        },
        {
            "nombre": "Cafetera automática",
            "caracteristicas": ["15 bares", "Cappuccino", "Espresso"]
        }
    ]
    
    resultados_exitosos = 0
    
    for i, producto in enumerate(productos_ejemplo, 1):
        print(f"\n📝 Producto {i}: {producto['nombre']}")
        print(f"   Keywords: {', '.join(producto['caracteristicas'])}")
        
        print(f"\n🔄 Generando título SEO...")
        inicio = time.time()
        
        resultado = modelo.generar_titulo_producto(
            nombre_base=producto['nombre'],
            caracteristicas=producto['caracteristicas']
        )
        
        tiempo = time.time() - inicio
        
        if resultado['success']:
            titulo = resultado['titulo']
            print(f"✅ Título generado en {tiempo:.2f}s:")
            print(f"\n   🏷️ {titulo}")
            print(f"   📏 Longitud: {len(titulo)} caracteres (recomendado: <60)")
            resultados_exitosos += 1
        else:
            print(f"❌ Error: {resultado.get('error', 'Desconocido')}")
        
        print("-" * 70)
    
    print(f"\n📊 RESUMEN: {resultados_exitosos}/{len(productos_ejemplo)} títulos generados exitosamente")
    return resultados_exitosos == len(productos_ejemplo)


def test_templates():
    """Prueba 6: Sistema de templates."""
    separador("PRUEBA 6: SISTEMA DE TEMPLATES", "=")
    
    print("📋 Categorías de templates disponibles:")
    categorias = PromptTemplates.listar_categorias()
    for i, cat in enumerate(categorias, 1):
        print(f"   {i}. {cat.capitalize()}")
    
    print(f"\n✅ Total: {len(categorias)} templates disponibles")
    
    # Probar construcción de prompt
    print("\n🔨 Probando construcción de prompt personalizado...")
    
    datos_ejemplo = {
        "nombre": "Camiseta básica premium",
        "caracteristicas": "Algodón peinado, corte regular",
        "talla": "L",
        "material": "100% algodón",
        "color": "Negro"
    }
    
    prompt = PromptTemplates.construir_prompt_personalizado("ropa", datos_ejemplo)
    
    print("\n📝 Prompt generado:")
    print("-" * 70)
    print(prompt)
    print("-" * 70)
    
    return True


def test_rendimiento(modelo):
    """Prueba 7: Test de rendimiento."""
    separador("PRUEBA 7: RENDIMIENTO", "=")
    
    print("⏱️ Midiendo tiempos de respuesta...")
    
    tiempos = []
    n_tests = 5
    
    for i in range(n_tests):
        print(f"\n   Test {i+1}/{n_tests}...", end=" ")
        
        inicio = time.time()
        resultado = modelo.generar_descripcion_producto(
            nombre_producto=f"Producto de prueba {i+1}",
            caracteristicas=["Característica 1", "Característica 2"]
        )
        tiempo = time.time() - inicio
        
        tiempos.append(tiempo)
        print(f"✅ {tiempo:.2f}s")
    
    # Estadísticas
    tiempo_promedio = sum(tiempos) / len(tiempos)
    tiempo_min = min(tiempos)
    tiempo_max = max(tiempos)
    
    print(f"\n📊 ESTADÍSTICAS DE RENDIMIENTO:")
    print(f"   ⏱️ Tiempo promedio: {tiempo_promedio:.2f}s")
    print(f"   🏃 Más rápido: {tiempo_min:.2f}s")
    print(f"   🐌 Más lento: {tiempo_max:.2f}s")
    
    # Evaluación
    if tiempo_promedio < 3:
        print(f"   ✅ Excelente rendimiento!")
    elif tiempo_promedio < 5:
        print(f"   ✅ Buen rendimiento")
    else:
        print(f"   ⚠️ Rendimiento mejorable")
    
    return True


def ejecutar_todas_las_pruebas():
    """Ejecuta todas las pruebas del módulo."""
    separador("SUITE DE PRUEBAS COMPLETA", "█")
    
    print("🚀 ComprIAssist - Módulo de IA Generativa")
    print("📅 Fecha:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print("\nEjecutando suite completa de pruebas...\n")
    
    resultados = {}
    
    # Prueba 1: Configuración
    resultados["Configuración"] = test_configuracion()
    
    # Prueba 2: Modelo
    modelo = test_modelo_basico()
    resultados["Inicialización"] = modelo is not None
    
    if modelo:
        # Prueba 3: Descripciones
        resultados["Descripciones"] = test_descripcion_producto(modelo)
        
        # Prueba 4: Chatbot
        resultados["Chatbot"] = test_chatbot(modelo)
        
        # Prueba 5: Títulos SEO
        resultados["Títulos SEO"] = test_titulo_seo(modelo)
        
        # Prueba 6: Templates
        resultados["Templates"] = test_templates()
        
        # Prueba 7: Rendimiento
        resultados["Rendimiento"] = test_rendimiento(modelo)
    
    # Resumen final
    separador("RESUMEN FINAL", "█")
    
    total = len(resultados)
    exitosos = sum(1 for v in resultados.values() if v)
    
    print("📊 RESULTADOS DE PRUEBAS:\n")
    
    for nombre, resultado in resultados.items():
        icono = "✅" if resultado else "❌"
        print(f"   {icono} {nombre}")
    
    print(f"\n{'='*70}")
    print(f"   TOTAL: {exitosos}/{total} pruebas exitosas ({exitosos/total*100:.1f}%)")
    print(f"{'='*70}")
    
    if exitosos == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON! El módulo está listo para usar.")
    elif exitosos >= total * 0.7:
        print("\n✅ Mayoría de pruebas pasaron. Revisar fallos menores.")
    else:
        print("\n⚠️ Varias pruebas fallaron. Revisar configuración.")
    
    return exitosos == total


if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║           COMPRIASSIST - MÓDULO IA GENERATIVA                     ║
║           Suite de Pruebas Automatizada                           ║
║                                                                   ║
║           Universidad Privada Antenor Orrego                      ║
║           Ingeniería de Sistemas e IA                             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
    """)
    
    try:
        exito = ejecutar_todas_las_pruebas()
        sys.exit(0 if exito else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error fatal: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
