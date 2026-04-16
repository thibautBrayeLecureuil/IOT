import json
import paho.mqtt.client as mqtt
import tkinter as tk
import sys
from datetime import datetime
from time import sleep

#Configuration du config.json
with open("config.json", "r") as f:
    data = json.load(f)

TYPE_MSG = 'Messages'
TYPE_ERROR = 'Error'
METRICS = 'METRICS'

TEMPERATURE = 'TEMPERATURE'
HUMIDITY= 'HUMIDITY'
LIGHT = 'LIGHT'
SOUND = 'SOUND'
TIMESTAMP = "TIMESTAMP"

#Juste des variables
broker = data['mqtt']['broker']
port = data['mqtt']['port']
topics = data['mqtt']['topics']
devices = {}
components = {}

def on_connect(client, userdata, flags, rc):
    for topic in topics:
        client.subscribe(topic) #On s'abonne aux topics
        print(f"abonné à : {topic}")

def update_device(mac_address, msgType, metrics,timestamp):
    if mac_address in devices :
        devices[mac_address][msgType] += 1
        devices[mac_address][METRICS] = metrics
        devices[mac_address][TIMESTAMP] = timestamp
    else :
        devices[mac_address] = {TYPE_MSG : 1, TYPE_ERROR : 0, METRICS : metrics, TIMESTAMP : timestamp}

def update_supervis_data(mac_source):

    metrics = devices[mac_source][METRICS]

    if TEMPERATURE in metrics:
        update_display_component(mac_source,TEMPERATURE, f"Température : {metrics[TEMPERATURE]} °C")
        #var_hum.set(f"Température : {metrics[TEMPERATURE]} °C")
    if HUMIDITY in metrics:
        update_display_component(mac_source, HUMIDITY, f"Humidité : {metrics[HUMIDITY]} %")
        #var_hum.set(f"Humidité : {metric} %")
    if LIGHT in metrics:
        update_display_component(mac_source, LIGHT, f"Lumière : {metrics[LIGHT]}")
        #var_light.set(f"Lumière : {metric}")
    if SOUND in metrics:
        update_display_component(mac_source, SOUND, f"Son : {metrics[SOUND]}")
        #var_sound.set(f"Son : {metric}")

def update_display_component(mac_address, TYPE, value):
    if mac_address not in components :
        components[mac_address] = {}
        components[mac_address]["TITLE"] = tk.StringVar(value=mac_address)
        tk.Label(window, textvariable=components[mac_address]["TITLE"], width=25).pack(pady=5)
    
    if TYPE in components[mac_address] :
        components[mac_address][TYPE].set(value) 
    else :
        components[mac_address][TYPE] = tk.StringVar(value=value)
        tk.Label(window, textvariable=components[mac_address][TYPE], width=25).pack(pady=5)



def error_percent(mac_source):

    nbError = devices[mac_source][TYPE_ERROR]
    nbMessage = devices[mac_source][TYPE_MSG]

    return nbError/nbMessage*100
        
def check_connections():
    for device in devices:
        if device[TIMESTAMP] - datetime.now().isoformat():
            components.pop(device)

def on_message(client, userdata, msg):
    try:
        payload_str = json.loads(msg.payload.decode("utf-8")) #On déchiffre le message reçu
        mac_source = payload_str.get("MAC_ADDRESS")
        
        timestamp = payload_str.get(TIMESTAMP)
       
        metrics = payload_str.get(METRICS)

        update_device(mac_source, TYPE_MSG, metrics, timestamp)

        #On vérifie quelles données sont présentes
        update_supervis_data(mac_source)
        
    except Exception as e:
        devices[mac_source][TYPE_ERROR]+=1
        #update_device(mac_source, TYPE_ERROR, None)
        print(f"Erreur : {e}","oui")
        if error_percent(mac_source) >= 5:
            #Preparation du message d'erreur
            """ack_payload = json.dumps({
                "target_mac": mac_source,
                "status": "Erreur supérieur à 5%",
                "timestamp": datetime.now().isoformat()
            })
            client.publish(msg.topic, ack_payload)
            print(f"message d'erreur envoyé vers {msg.topic}")"""

    check_connections()


window = tk.Tk()
window.title("Supervision Météo")
window.geometry("400x350")

tk.Label(window, text="Station Météo Distribuée", font=("Helvetica", 18, "bold"), fg="white", bg="#2c3e50").pack(pady=15)

"""var_temp = tk.StringVar(value="Température : -- °C")
var_hum = tk.StringVar(value="Humidité : -- %")
var_light = tk.StringVar(value="Lumière : --")
var_sound = tk.StringVar(value="Son : --")"""

"""tk.Label(window, textvariable=var_temp, width=25).pack(pady=5)
tk.Label(window, textvariable=var_hum, width=25).pack(pady=5)
tk.Label(window, textvariable=var_light, width=25).pack(pady=5)
tk.Label(window, textvariable=var_sound, width=25).pack(pady=5)"""

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
client.loop_start()
window.mainloop()
client.loop_stop()
client.disconnect()