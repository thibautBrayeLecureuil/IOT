import adafruit_dht
from board import <pin>

dht_device = adafruit_dht.DHT11(<pin>)


def main():
    temperature = dht_device.temperature
    humidity = dht_device.humidity
    print("Humidity:", humidity)
    print("Temperature:", temperature)
    print("================================")

if __name__ == "__main__":
    main()
