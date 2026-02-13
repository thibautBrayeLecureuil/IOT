from time import sleep

import adafruit_dht
import board
import time

dhtDevice = adafruit_dht.DHT11(board.D2)


def main():
    while(True):
        try:
            dhtDevice.measure()
            print("Humidity:", dhtDevice.humidity)
            print("Temperature:", dhtDevice.temperature)
        except RuntimeError:
            print("Petite erreur on revient vite 😊")
        print("================================")
        sleep(5)



if __name__ == "__main__":
    main()
