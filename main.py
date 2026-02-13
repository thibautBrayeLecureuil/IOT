import adafruit_dht
import board

dhtDevice = adafruit_dht.DHT11(board.D2)


def main():

    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity
    print("Humidity:", humidity)
    print("Temperature:", temperature)
    print("================================")

if __name__ == "__main__":
    main()
