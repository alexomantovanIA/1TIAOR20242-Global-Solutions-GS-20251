
import paho.mqtt.client as mqtt
import json
import random
import time

# Configuração do broker
broker = "mqtt.eclipseprojects.io"
port = 1883
topic = "esp32/sensores"

# Conecta ao broker
client = mqtt.Client()
client.connect(broker, port, 60)

def gerar_dado_simulado():
    return {
        "pot1": random.randint(0, 4096),        # Simula inclinômetro
        "pot2": random.randint(0, 4096),        # Simula sensor de chuva
        "ax": random.randint(-16000, 16000),    # Simula vibração eixo X
        "ay": random.randint(-16000, 16000),    # Simula vibração eixo Y
        "az": random.randint(-16000, 16000),    # Simula vibração eixo Z
    }

# Envia dados continuamente (Ctrl+C para parar)
try:
    while True:
        dado = gerar_dado_simulado()
        payload = json.dumps(dado)
        client.publish(topic, payload)
        print("Publicado:", payload)
        time.sleep(2)  # Envia a cada 2 segundos
except KeyboardInterrupt:
    print("Interrompido pelo usuário.")
    client.disconnect()
