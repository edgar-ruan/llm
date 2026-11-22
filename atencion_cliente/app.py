"""
SoporteBot - Sistema de atención al cliente automatizado con la API de OpenAI.

Tienda ficticia: "TecnoMarket" (venta de electrónicos en línea).
- Responde preguntas frecuentes (envíos, devoluciones, pagos, garantías).
- Consulta el estado de un pedido cuando el cliente da su número (base de datos simulada).
- Recomienda productos del catálogo.
- Si el cliente lo pide o está muy molesto, crea un ticket para un agente humano (simulado).
"""
import os
import re
import random

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODELO = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ---------------- Datos simulados ----------------
PEDIDOS = {
    "1001": {"cliente": "Laura", "producto": "Audífonos Bluetooth X200", "estado": "En camino", "entrega": "2 días hábiles"},
    "1002": {"cliente": "Carlos", "producto": "Laptop Pro 14", "estado": "Entregado", "entrega": "Entregado el 15 de noviembre"},
    "1003": {"cliente": "Sofía", "producto": "Smartwatch Fit 3", "estado": "Preparando envío", "entrega": "4-5 días hábiles"},
    "1004": {"cliente": "Miguel", "producto": "Monitor 27\" 4K", "estado": "Retrasado por paquetería", "entrega": "6-8 días hábiles"},
}

CATALOGO = """
- Audífonos Bluetooth X200: $899 MXN, cancelación de ruido, 30 h de batería.
- Laptop Pro 14: $18,999 MXN, 16 GB RAM, SSD 512 GB, ideal para trabajo y estudio.
- Smartwatch Fit 3: $2,499 MXN, monitoreo de ritmo cardiaco y sueño, resistente al agua.
- Monitor 27" 4K: $6,499 MXN, ideal para diseño y gaming.
- Teclado mecánico K87: $1,199 MXN, switches rojos, retroiluminado.
"""

INSTRUCCIONES = f"""
Eres SoporteBot, el asistente de atención al cliente de TecnoMarket, una tienda en línea de electrónicos en México.

Reglas:
- Responde siempre en español, de forma amable, clara y breve (máximo 4-5 oraciones).
- Solo hablas de temas de TecnoMarket. Si preguntan otra cosa, redirige amablemente.
- No inventes información de pedidos. Si te dan datos de un pedido en el mensaje del sistema, úsalos.
- Si el cliente quiere saber de su pedido y no te ha dado el número, pídeselo (son números de 4 dígitos).
- Si no sabes algo, dilo y ofrece comunicarlo con un agente humano.

Políticas de la tienda:
- Envíos: gratis en compras mayores a $999 MXN. Tiempo de entrega de 3 a 5 días hábiles.
- Devoluciones: 30 días después de recibir el producto, en su empaque original.
- Garantía: 1 año en todos los productos contra defectos de fábrica.
- Pagos: tarjeta de crédito/débito, PayPal y OXXO. Meses sin intereses en compras mayores a $3,000 MXN.
- Horario de agentes humanos: lunes a viernes de 9:00 a 18:00.

Catálogo:
{CATALOGO}
"""

PALABRAS_HUMANO = ["humano", "agente", "persona real", "asesor", "queja"]


# ---------------- Funciones simuladas ----------------
def consultar_pedido(numero):
    print(f"   🔎 Consultando base de datos de pedidos... (pedido #{numero})")
    return PEDIDOS.get(numero)


def crear_ticket(historial):
    ticket = random.randint(50000, 59999)
    print(f"   📝 Creando ticket #{ticket} y enviando la conversación a un agente humano...")
    return ticket


# ---------------- Lógica del chatbot ----------------
def preparar_contexto(mensaje):
    """Revisa el mensaje y agrega información extra para el modelo si hace falta."""
    extra = []

    numeros = re.findall(r"\b\d{4}\b", mensaje)
    for numero in numeros:
        pedido = consultar_pedido(numero)
        if pedido:
            extra.append(f"Datos del pedido #{numero}: {pedido}")
        else:
            extra.append(f"El pedido #{numero} no existe en la base de datos.")

    if any(p in mensaje.lower() for p in PALABRAS_HUMANO):
        ticket = crear_ticket(mensaje)
        extra.append(f"Se creó el ticket #{ticket} para un agente humano. Avísale al cliente y dile el horario de atención.")

    return extra


def responder(cliente, historial, mensaje):
    for info in preparar_contexto(mensaje):
        historial.append({"role": "system", "content": info})
    historial.append({"role": "user", "content": mensaje})

    respuesta = cliente.chat.completions.create(
        model=MODELO,
        messages=historial,
        temperature=0.4,
    )
    texto = respuesta.choices[0].message.content
    historial.append({"role": "assistant", "content": texto})
    return texto


def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ No se encontró OPENAI_API_KEY. Crea un archivo .env (ver README.md).")
        return

    cliente = OpenAI()
    historial = [{"role": "system", "content": INSTRUCCIONES}]

    print("=" * 55)
    print("  🤖 SoporteBot - Atención al cliente de TecnoMarket")
    print("  Escribe 'salir' para terminar.")
    print("=" * 55)
    print("SoporteBot: ¡Hola! Soy SoporteBot. ¿En qué te puedo ayudar hoy?\n")

    while True:
        mensaje = input("Tú: ").strip()
        if not mensaje:
            continue
        if mensaje.lower() in ["salir", "exit", "adios", "adiós"]:
            print("SoporteBot: ¡Gracias por contactar a TecnoMarket! Que tengas excelente día. 👋")
            break

        try:
            texto = responder(cliente, historial, mensaje)
            print(f"SoporteBot: {texto}\n")
        except Exception as e:
            print(f"⚠️  Ocurrió un error al contactar a OpenAI: {e}\n")


if __name__ == "__main__":
    main()
