import adafruit_dht
import board

dhtDevice = adafruit_dht.DHT11(board.D2)


def main():
    while(True):
        dhtDevice.measure()
        print("Humidity:", dhtDevice.humidity)
        print("Temperature:", dhtDevice.temperature)
        print("================================")

if __name__ == "__main__":
    main()
