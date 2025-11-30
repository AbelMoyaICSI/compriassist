from generative_model import GenerativeModel

modelo = GenerativeModel()

resultado = modelo.generar_descripcion_producto(
    nombre_producto="Camiseta Premium",
    caracteristicas=["100% algodón", "Talla M"],
    categoria="ropa"
)

print(f"Éxito: {resultado['success']}")
print(f"Descripción: {resultado['descripcion']}")