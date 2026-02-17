import datetime
import time
import grovepi
import math
import json
import paho.mqtt.client as mqtt
from getmac import get_mac_address

MQTT_BROKER = "87.106.23.178" 
MQTT_PORT = 1883
MQTT_TOPIC = "device/LS"

sound_sensor = 0 #port a0
light_sensor = 1 #port a1

grovepi.pinMode(sound_sensor, "INPUT")
grovepi.pinMode(light_sensor, "INPUT")

#config mqtt
client = mqtt.Client()

def sound_to_db(sound_value):
    if sound_value <= 1: 
        return 0
    return round(20 * math.log10(sound_value), 2)

def light_to_lux(light_value):
    if light_value == 0:
        return 0
    return round((light_value / 1023) * 500, 2)

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start() 
    print(f"Connecté au broker  {MQTT_BROKER}")
except ConnectionRefusedError:
    print("Impossible de se connecter au broker ")
    exit(1)

while True:
    try:
        #Obtenir les valeurs du capteur de lumière
        light_intensity = grovepi.analogRead(light_sensor)
        light_lux = light_to_lux(light_intensity)
        
        #obtenir les valeurs du capteur de son
        sound_level = grovepi.analogRead(sound_sensor)
        sound_db = sound_to_db(sound_level)
    
        payload = {
		"MAC_ADDRESS": get_mac_address(),
		"TIMESTAMP": datetime.datetime.now().isoformat(),
		"METRICS": {
			"LIGHT": light_lux,
			"SOUND": sound_db,
			
		}
	}
        
        client.publish(MQTT_TOPIC, json.dumps(payload))

        # Affichage console (pour débug)
        print(f"Envoi MQTT -> {payload}")
        
        time.sleep(10)
        
    except IOError:
        print("Erreur de lecture des capteurs")
    except KeyboardInterrupt:
        print("\nArrêt du programme")
        client.loop_stop()
        client.disconnect()
        break
        