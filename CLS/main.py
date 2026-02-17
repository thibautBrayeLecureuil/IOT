import time
import grovepi
import math
import json
import paho.mqtt.client as mqtt

MQTT_BROKER = "10.33.14.44" 
MQTT_PORT = 1883
MQTT_TOPIC = "device/LS"

sound_sensor = 0 #port a0
light_sensor = 1 #port a1

grovepi.pinMode(sound_sensor, "INPUT")
grovepi.pinMode(light_sensor, "INPUT")

# Conversion de la valeur du son en dB
def sound_to_db(value):
    # Convertir la valeur analogique (0-1023) en dB
    # Seuil de silence à ~300
    if value < 300:
        return 0
    db = 20 * math.log10(value / 10)
    return db

# Conversion de la valeur de la lumière en lux
def light_to_lux(value):
    # Convertir la valeur analogique (0-1023) en lux
    lux = value / 1023.0 * 10000 
    return lux

#config mqtt
client = mqtt.Client()

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
        
        sound_level = grovepi.analogRead(sound_sensor)
        sound_db = sound_to_db(sound_level)
        
        payload = {
            "light_raw": light_intensity,
            "light_lux": light_lux,
            "sound_raw": sound_level,
            "sound_db": sound_db
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
        