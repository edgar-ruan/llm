# 🤖 SoporteBot — Atención al cliente automatizada con LLM

Proyecto 3 del tema **7. LLM**: un chatbot de atención al cliente para **TecnoMarket**, una tienda en línea de electrónicos (ficticia), usando la **API de OpenAI**.

## ¿Qué hace?

- 💬 Responde preguntas frecuentes: envíos, devoluciones, garantía, formas de pago y horarios.
- 📦 Consulta el estado de un pedido cuando el cliente da su número (base de datos simulada).
- 🛒 Recomienda productos del catálogo según lo que necesita el cliente.
- 🧑‍💼 Si el cliente pide un agente humano o quiere poner una queja, crea un ticket (simulado).
- 🧠 Recuerda la conversación para responder con contexto.

## ¿Cómo funciona?

```
Mensaje del cliente
        │
        ▼
¿Trae número de pedido? ──sí──> 🔎 consulta la "base de datos" y agrega los datos al contexto
¿Pide un humano?        ──sí──> 📝 crea un ticket y lo agrega al contexto
        │
        ▼
OpenAI (gpt-4o-mini) con: instrucciones + políticas + catálogo + historial
        │
        ▼
Respuesta al cliente
```

Las instrucciones del sistema (*system prompt*) le dan al modelo las políticas de la tienda y el catálogo, y le indican que no invente datos de pedidos.

## Estructura

```
atencion_cliente/
├── app.py            # Chatbot
├── requirements.txt  # Dependencias
└── .env.example      # Ejemplo de variables de entorno
```

## Instalación

Requiere Python 3.9 o superior y una API key de OpenAI (https://platform.openai.com/api-keys).

```bash
# 1. Clonar el repositorio y entrar a la carpeta del proyecto
git clone https://github.com/edgar-ruan/llm.git
cd llm/atencion_cliente

# 2. Crear y activar entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar la API key
#    Copia .env.example a .env y pon tu API key
#    Windows:  copy .env.example .env
#    Mac/Linux: cp .env.example .env
```

## Uso

```bash
python app.py
```

Pedidos de prueba: **1001**, **1002**, **1003** y **1004**.

## Ejemplo de conversación

```
SoporteBot: ¡Hola! Soy SoporteBot. ¿En qué te puedo ayudar hoy?

Tú: hola, quiero saber dónde está mi pedido 1004
   🔎 Consultando base de datos de pedidos... (pedido #1004)
SoporteBot: Hola, Miguel. Tu Monitor 27" 4K está retrasado por la paquetería.
La nueva fecha estimada es de 6 a 8 días hábiles. Lamentamos la demora.

Tú: ¿y puedo devolverlo si no me gusta?
SoporteBot: Claro, tienes 30 días después de recibirlo para devolverlo en su empaque original.

Tú: quiero hablar con un agente
   📝 Creando ticket #53120 y enviando la conversación a un agente humano...
SoporteBot: Listo, creé el ticket #53120. Un agente te contactará en horario de
lunes a viernes de 9:00 a 18:00.
```

## Tecnologías
- Python
- OpenAI API (`gpt-4o-mini`)
- python-dotenv

> Nota: la carpeta `asistente_escritura/` viene del repositorio original del curso.
