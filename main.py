import adafruit_dht

DHT_PIN = 2
DHT_SENSOR = adafruit_dht.DHT11


def main():
    humidity, temperature = adafruit_dht.read(DHT_SENSOR, DHT_PIN)
    print("Humidity:", humidity)
    print("Temperature:", temperature)
    print("================================")

if __name__ == "__main__":
    main()
