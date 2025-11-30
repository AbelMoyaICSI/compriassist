"""
Probador Interactivo de API Generativa - ComprIAssist
Ejecutar: python test_interactive.py
"""

import requests
import json
from datetime import datetime
import time


class Colors:
    """Colores para la terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")


def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")


def print_info(text):
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.ENDC}")


def print_json(data):
    """Imprime JSON con formato y colores"""
    print(f"{Colors.YELLOW}{json.dumps(data, indent=2, ensure_ascii=False)}{Colors.ENDC}")


def test_endpoint(name, method, url, data=None):
    """Prueba un endpoint y muestra el resultado"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}📍 {name}{Colors.ENDC}")
    print(f"{Colors.CYAN}   {method} {url}{Colors.ENDC}")
    
    if data:
        print(f"\n{Colors.BOLD}📤 Request Body:{Colors.ENDC}")
        print_json(data)
    
    try:
        start_time = time.time()
        
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        elapsed = time.time() - start_time
        
        print(f"\n{Colors.BOLD}📥 Response:{Colors.ENDC}")
        print(f"   Status Code: {Colors.GREEN if response.status_code == 200 else Colors.RED}{response.status_code}{Colors.ENDC}")
        print(f"   Tiempo: {Colors.CYAN}{elapsed:.2f}s{Colors.ENDC}")
        
        try:
            response_data = response.json()
            print(f"\n{Colors.BOLD}📄 Response Body:{Colors.ENDC}")
            print_json(response_data)
            
            # Mostrar información específica según el endpoint
            if response.status_code == 200 and response_data.get('success'):
                if 'descripcion' in str(response_data):
                    desc = response_data.get('data', {}).get('descripcion', '')
                    if desc:
                        print(f"\n{Colors.GREEN}{Colors.BOLD}📝 Descripción Generada:{Colors.ENDC}")
                        print(f"{Colors.GREEN}   {desc}{Colors.ENDC}")
                
                if 'respuesta' in str(response_data):
                    resp = response_data.get('data', {}).get('respuesta', '')
                    if resp:
                        print(f"\n{Colors.GREEN}{Colors.BOLD}💬 Respuesta del Chatbot:{Colors.ENDC}")
                        print(f"{Colors.GREEN}   {resp}{Colors.ENDC}")
                
                if 'titulo' in str(response_data):
                    titulo = response_data.get('data', {}).get('titulo', '')
                    if titulo:
                        print(f"\n{Colors.GREEN}{Colors.BOLD}🏷️  Título SEO:{Colors.ENDC}")
                        print(f"{Colors.GREEN}   {titulo}{Colors.ENDC}")
            
            return response.status_code == 200
            
        except json.JSONDecodeError:
            print(f"\n{Colors.RED}Response Text:{Colors.ENDC}")
            print(response.text[:500])
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("No se pudo conectar al servidor")
        print_info("Asegúrate de que el servidor esté corriendo: python server.py")
        return False
    except requests.exceptions.Timeout:
        print_error("Timeout - El servidor no respondió a tiempo")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def main():
    """Función principal"""
    print(f"""
{Colors.BOLD}{Colors.CYAN}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║         COMPRIASSIST - PROBADOR INTERACTIVO API                   ║
║              Módulo de IA Generativa                              ║
║                                                                   ║
║              Universidad Privada Antenor Orrego                   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.ENDC}
    """)
    
    BASE_URL = "http://localhost:8000"
    
    # Verificar servidor
    print_header("VERIFICANDO SERVIDOR")
    print_info("Verificando que el servidor esté activo...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/generative/", timeout=5)
        print_success("Servidor activo y respondiendo")
    except:
        print_error("Servidor no responde")
        print_info("Inicia el servidor con: python server.py")
        return
    
    # Resultados
    resultados = {}
    
    # TEST 1: Info General
    print_header("TEST 1: INFORMACIÓN GENERAL")
    resultados['Info General'] = test_endpoint(
        "Información del Módulo",
        "GET",
        f"{BASE_URL}/api/generative/"
    )
    input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.ENDC}")
    
    # TEST 2: Generar Descripción - Ropa
    print_header("TEST 2: GENERAR DESCRIPCIÓN - ROPA")
    resultados['Descripción Ropa'] = test_endpoint(
        "Descripción de Camiseta",
        "POST",
        f"{BASE_URL}/api/generative/generar-descripcion",
        {
            "nombre_producto": "Camiseta de algodón orgánico Premium",
            "caracteristicas": [
                "100% algodón orgánico certificado",
                "Talla M",
                "Color azul marino",
                "Eco-friendly",
                "Secado rápido"
            ],
            "categoria": "ropa",
            "precio": 29.99,
            "temperatura": 0.7
        }
    )
    input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.ENDC}")
    
    # TEST 3: Generar Descripción - Electrónica
    print_header("TEST 3: GENERAR DESCRIPCIÓN - ELECTRÓNICA")
    resultados['Descripción Electrónica'] = test_endpoint(
        "Descripción de Auriculares",
        "POST",
        f"{BASE_URL}/api/generative/generar-descripcion",
        {
            "nombre_producto": "Auriculares Bluetooth Premium ANC",
            "caracteristicas": [
                "Cancelación de ruido activa",
                "30 horas de batería",
                "Bluetooth 5.2",
                "Micrófono HD",
                "Estuche de carga incluido"
            ],
            "categoria": "electronica",
            "precio": 79.99,
            "temperatura": 0.7
        }
    )
    input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.ENDC}")
    
    # TEST 4: Generar Descripción - Deportes
    print_header("TEST 4: GENERAR DESCRIPCIÓN - DEPORTES")
    resultados['Descripción Deportes'] = test_endpoint(
        "Descripción de Zapatillas",
        "POST",
        f"{BASE_URL}/api/generative/generar-descripcion",
        {
            "nombre_producto": "Zapatillas Running Pro Max",
            "caracteristicas": [
                "Amortiguación avanzada",
                "Transpirables",
                "Suela antideslizante",
                "Diseño ergonómico"
            ],
            "categoria": "deportes",
            "precio": 89.99
        }
    )
    input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.ENDC}")
    
    # TEST 5: Chatbot - Pregunta sobre productos
    print_header("TEST 5: CHATBOT - CONSULTA DE PRODUCTOS")
    resultados['Chatbot Productos'] = test_endpoint(
        "Consulta sobre ropa de verano",
        "POST",
        f"{BASE_URL}/api/generative/chatbot-respuesta",
        {
            "pregunta": "¿Tienen ropa para verano? Busco algo fresco y cómodo",
            "contexto": "Usuario busca ropa casual para clima cálido"
        }
    )
    input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.ENDC}")
    
    # TEST 6: Chatbot - Pregunta sobre envío
    print_header("TEST 6: CHATBOT - CONSULTA DE ENVÍO")
    resultados['Chatbot Envío'] = test_endpoint(
        "Consulta sobre costos de envío",
        "POST",
        f"{BASE_URL}/api/generative/chatbot-respuesta",
        {
            "pregunta": "¿Cuánto cuesta el envío? ¿Tienen envío gratis?",
            "contexto": "Usuario pregunta sobre logística y costos"
        }
    )
    input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.ENDC}")
    
    # TEST 7: Chatbot - Pregunta sobre devoluciones
    print_header("TEST 7: CHATBOT - CONSULTA DE DEVOLUCIONES")
    resultados['Chatbot Devoluciones'] = test_endpoint(
        "Consulta sobre políticas de devolución",
        "POST",
        f"{BASE_URL}/api/generative/chatbot-respuesta",
        {
            "pregunta": "¿Puedo devolver un producto si no me gusta?",
            "contexto": "Usuario tiene dudas sobre políticas"
        }
    )
    input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.ENDC}")
    
    # TEST 8: Título SEO
    print_header("TEST 8: GENERAR TÍTULO SEO")
    resultados['Título SEO'] = test_endpoint(
        "Título optimizado para buscadores",
        "POST",
        f"{BASE_URL}/api/generative/generar-titulo-seo",
        {
            "nombre_base": "Zapatillas deportivas Nike Air Max",
            "caracteristicas": ["Running", "Amortiguación", "Transpirables", "Premium"]
        }
    )
    input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.ENDC}")
    
    # TEST 9: Generación en Lote
    print_header("TEST 9: GENERACIÓN EN LOTE")
    resultados['Generación Batch'] = test_endpoint(
        "Múltiples descripciones simultáneas",
        "POST",
        f"{BASE_URL}/api/generative/generar-batch",
        {
            "productos": [
                {
                    "nombre_producto": "Camiseta básica",
                    "caracteristicas": ["Algodón", "Talla M"],
                    "categoria": "ropa",
                    "precio": 19.99
                },
                {
                    "nombre_producto": "Auriculares Bluetooth",
                    "caracteristicas": ["Cancelación de ruido", "30h batería"],
                    "categoria": "electronica",
                    "precio": 79.99
                },
                {
                    "nombre_producto": "Zapatillas Running",
                    "caracteristicas": ["Amortiguación", "Transpirables"],
                    "categoria": "deportes",
                    "precio": 89.99
                }
            ]
        }
    )
    input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.ENDC}")
    
    # TEST 10: Templates
    print_header("TEST 10: OBTENER TEMPLATES")
    resultados['Templates'] = test_endpoint(
        "Templates disponibles por categoría",
        "GET",
        f"{BASE_URL}/api/generative/templates"
    )
    input(f"\n{Colors.YELLOW}Presiona Enter para continuar...{Colors.ENDC}")
    
    # TEST 11: Health Check
    print_header("TEST 11: HEALTH CHECK")
    resultados['Health Check'] = test_endpoint(
        "Estado del servicio",
        "GET",
        f"{BASE_URL}/api/generative/health"
    )
    
    # RESUMEN FINAL
    print_header("📊 RESUMEN DE PRUEBAS")
    
    exitosos = sum(1 for r in resultados.values() if r)
    total = len(resultados)
    porcentaje = (exitosos / total * 100) if total > 0 else 0
    
    print(f"\n{Colors.BOLD}Resultados Detallados:{Colors.ENDC}\n")
    
    for nombre, resultado in resultados.items():
        if resultado:
            print(f"  {Colors.GREEN}✅ {nombre}{Colors.ENDC}")
        else:
            print(f"  {Colors.RED}❌ {nombre}{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}  TOTAL: {Colors.CYAN}{exitosos}/{total}{Colors.ENDC} {Colors.BOLD}pruebas exitosas ({porcentaje:.1f}%){Colors.ENDC}")
    print(f"{Colors.BOLD}{'='*70}{Colors.ENDC}\n")
    
    if exitosos == total:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 ¡EXCELENTE! Todos los endpoints funcionan correctamente{Colors.ENDC}")
    elif exitosos >= total * 0.8:
        print(f"{Colors.YELLOW}{Colors.BOLD}✅ Muy bien! La mayoría de endpoints funcionan{Colors.ENDC}")
    elif exitosos >= total * 0.5:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  Algunos endpoints tienen problemas{Colors.ENDC}")
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ Varios endpoints fallaron. Revisa la configuración{Colors.ENDC}")
    
    print(f"\n{Colors.CYAN}Fecha de prueba: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Pruebas interrumpidas por el usuario{Colors.ENDC}")
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ Error fatal: {str(e)}{Colors.ENDC}")
        import traceback
        traceback.print_exc()