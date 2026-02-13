import adafruit_dht
import board

pin_to_use = "GPIO2"

def main():

    dhtDevice = adafruit_dht.DHT11(pin=getattr(board, pin_to_use))
    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity
    print("Humidity:", humidity)
    print("Temperature:", temperature)
    print("================================")

if __name__ == "__main__":
    main()
