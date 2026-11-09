from datetime import datetime
import paho.mqtt.client as mqtt
import requests

# --- CONFIGURAÇÕES ---
# ⚠️ Cole aqui a URL completa do seu Firebase (MANTENHA o '/leituras.json' no final)
FIREBASE_URL = (
    "https://SEU-PROJETO-AQUI.firebaseio.com/leituras.json"
)

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "projeto/iot/pinage/temperatura/2026"


def ao_conectar(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Conectado ao Broker com sucesso!")
        client.subscribe(MQTT_TOPIC)
        print(f"Escutando o tópico: {MQTT_TOPIC}\n")
    else:
        print(f"Falha ao conectar. Código de erro: {reason_code}")


def ao_receber_mensagem(client, userdata, msg):
    try:
        # Decodifica a temperatura da ESP32
        temperatura_recebida = float(msg.payload.decode("utf-8"))

        # Pega a data e hora
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Pacote de dados para a nuvem
        dados = {"temperatura": temperatura_recebida, "timestamp": agora}

        # Em vez de salvar no TXT, enviamos para o Firebase:
        resposta = requests.post(FIREBASE_URL, json=dados)

        if resposta.status_code == 200:
            print(
                f"🔥 Salvo no Firebase com sucesso! -> {agora} |"
                f" {temperatura_recebida} °C"
            )
        else:
            print(f"⚠️ Erro ao enviar para o Firebase: {resposta.status_code}")

    except ValueError:
        print(f"Dado inválido recebido: {msg.payload.decode('utf-8')}")


# --- LÓGICA PRINCIPAL ---
cliente_mqtt = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
cliente_mqtt.on_connect = ao_conectar
cliente_mqtt.on_message = ao_receber_mensagem

print(f"Tentando conectar ao servidor {MQTT_BROKER}...")
cliente_mqtt.connect(MQTT_BROKER, MQTT_PORT)

try:
    cliente_mqtt.loop_forever()
except KeyboardInterrupt:
    print("\nPrograma encerrado pelo usuário.")
    cliente_mqtt.disconnect()