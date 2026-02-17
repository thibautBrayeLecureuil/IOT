from time import sleep
import adafruit_dht
import board
import time
import socket
import paho.mqtt.client as mqtt
import datetime
from getmac import get_mac_address
import json

dhtDevice = adafruit_dht.DHT11(board.D2)

BROKER = "10.33.14.44"
PORT = 1883
DEVICE_ID = socket.gethostname()
TOPIC = f"HT"

client = mqtt.Client(
 mqtt.CallbackAPIVersion.VERSION2,
 client_id=f"sensor-{DEVICE_ID}"
)
client.connect(BROKER, PORT)
print(f"Connecté au broker {BROKER}:{PORT}")



def main():
    while(True):
        try:
            dhtDevice.measure()
            print("Humidity:", dhtDevice.humidity)
            print("Temperature:", dhtDevice.temperature)

            timestamp = datetime.datetime.now().isoformat()

            data = {
                "MAC_ADDRESS": get_mac_address(),
                "TIMESTAMP": timestamp,
                "METRICS": {
                    "TEMPERATURE": dhtDevice.temperature,
                    "HUMIDITY": dhtDevice.humidity,
                }
            }

            topic = f"LTH/{TOPIC}"

            # PART 5
            client.publish(topic, json.dumps(data))

        except RuntimeError:
            print("Petite erreur on revient vite 😊")
        print("================================")
        sleep(60)

if __name__ == "__main__":
    main()
