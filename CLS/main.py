import time
import grovepi
import math

#Connections

sound_sensor = 0 #port a0
light_sensor = 1 #port a1
led = 3 #port D3

last_sound = 0
last_light = 0
grovepi.pinMode(led,"OUTPUT")

while True:
    try:
        #Obtenir les valeurs du capteur de lumière
        light_intensity = grovepi.analogRead(light_sensor,"INPUT")
        
        #Obtenir les valeurs du capteur de son
        sound_level = grovepi.analogRead(sound_sensor,"INPUT")
        if sound_level > 0:
            last_sound = sound_level
            
        #Afficher les valeurs
        print("Light Intensity: {}".format(light_intensity))
        print("Sound Level: {}".format(sound_level))
        print("Last Sound Level: {}".format(last_sound))
        if light_intensity > 500:
            grovepi.digitalWrite(led,1) #Allumer la LED
        else:
            grovepi.digitalWrite(led,0) #Éteindre la LED
        time.sleep(1)
    except IOError:
        print("Erreur de lecture des capteurs")
        