import json
import paho.mqtt.client as mqtt
import tkinter as tk
import sys

#Configuration du config.json
with open("config.json", "r") as f:
    data = json.load(f)

#Juste des variables
broker = data['mqtt']['broker']
port = data['mqtt']['port']
topics = data['mqtt']['topics']
acktopic = data['mqtt']['ack_topic']

def on_connect(client, userdata, flags, rc):
    for topic in topics:
        client.subscribe(topic) #On s'abonne aux topics
        print(f"abonné à : {topic}")

def on_message(client, userdata, msg):
    try:
        payload_str = json.loads(msg.payload.decode("utf-8")) #On déchiffre le message reçu
        time = payload_str.get("TIMESTAMP")
        mac_source = payload_str.get("MAC_ADDRESS")
        metrics = payload_str.get('METRICS')
        #print(f"Message reçu de {mac_source} sur {msg.topic} :")
        #print(f"Données : {metrics}")

        #On vérifie quelles données sont présentes
        if "TEMPERATURE" in metrics:
            var_temp.set(f"Température : {metrics['TEMPERATURE']} °C")
        if "HUMIDITY" in metrics:
            var_hum.set(f"Humidité : {metrics['HUMIDITY']} %")
        if "LIGHT" in metrics:
            var_light.set(f"Lumière : {metrics['LIGHT']}")
        if "SOUND" in metrics:
            var_sound.set(f"Son : {metrics['SOUND']}")

        #Preparation du message d'acquittement
        ack_payload = json.dumps({
            "target_mac": mac_source,
            "status": "OK",
            "timestamp": payload_str.get("TIMESTAMP")
        })

        #Envoie de l'aquittement
        client.publish(acktopic, ack_payload)
        print(f"ACK envoyé vers {acktopic}")
    except Exception as e:
        print(f"Erreur : {e}")    

window = tk.Tk()
window.title("Supervision Météo")
window.geometry("400x350")

tk.Label(window, text="Station Météo Distribuée", font=("Helvetica", 18, "bold"), fg="white", bg="#2c3e50").pack(pady=15)

var_temp = tk.StringVar(value="Température : -- °C")
var_hum = tk.StringVar(value="Humidité : -- %")
var_light = tk.StringVar(value="Lumière : --")
var_sound = tk.StringVar(value="Son : --")

tk.Label(window, textvariable=var_temp, width=25).pack(pady=5)
tk.Label(window, textvariable=var_hum, width=25).pack(pady=5)
tk.Label(window, textvariable=var_light, width=25).pack(pady=5)
tk.Label(window, textvariable=var_sound, width=25).pack(pady=5)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
client.loop_start()
window.mainloop()
client.loop_stop()
client.disconnect()