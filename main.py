from time import sleep

import adafruit_dht
import board
import time

dhtDevice = adafruit_dht.DHT11(board.D2)


def main():
    while(True):
        dhtDevice.measure()
        print("Humidity:", dhtDevice.humidity)
        print("Temperature:", dhtDevice.temperature)
        print("================================")
        sleep(10)

if __name__ == "__main__":
    main()
