📋 Projet IoT : Station de Surveillance Environnementale (LS & HT)
1. Présentation du Projet

Ce projet consiste en une solution de monitoring en temps réel de l'environnement (Lumière, Son, Température et Humidité). Il utilise une architecture MQTT où des Raspberry Pi jouent le rôle d'émetteurs (Publishers) et un ordinateur central joue le rôle de récepteur (Subscriber) via un tableau de bord graphique.
2. Architecture Technique

    Hardware :

        Raspberry Pi 3B+ avec carte GrovePi+.

        Capteurs : Son (A0), Lumière (A1), DHT11 (D2).

    Protocole : MQTT (Broker Mosquitto).

    Format des données : JSON (Standardisé avec MAC Address et Timestamp).

    Lancement : Service Linux systemd pour un démarrage automatisé "Plug & Play".

3. Installation
Émetteurs (Raspberry Pi)

    Installez les dépendances Python nécessaires :
    Bash

    pip3 install paho-mqtt getmac adafruit-circuitpython-dht

    Placez les scripts main.py (Dossier CLS) et main.py ( Dossier DHT) dans le dossier /home/pi/Projet/.

    Configurez l'adresse IP du Broker dans les fichiers (par défaut 10.33.14.44).

Récepteur (PC de contrôle)

    Installez Python et la bibliothèque paho-mqtt.

    Assurez-vous que le fichier config.json contient l'adresse IP correcte du Broker.

    Lancez l'interface de supervision :
    Bash

    python3 main.py (Dossier BROKER)

4. Configuration Systemd

Pour assurer la continuité de service, le script est géré par un service système :

    Fichier : /etc/systemd/system/capteurs.service

    Commandes utiles :

        sudo systemctl start capteurs.service : Démarrer manuellement.

        sudo systemctl enable capteurs.service : Activer au démarrage.

        sudo journalctl -u capteurs.service -f : Voir les logs en direct.

5. Spécifications du Payload MQTT

Les messages sont envoyés sur les topics LTH/LS (toutes les 10s) et LTH/HT (toutes les 60s) au format suivant :
JSON

{
    "MAC_ADDRESS": "b8:27:eb:aa:94:4b",
    "TIMESTAMP": "2026-02-17T16:23:06",
    "METRICS": {
        "LIGHT": 374.39,
        "SOUND": 37.73,
        "TEMPERATURE": 22.5,
        "HUMIDITY": 45.0
    }
}

6. Choix Techniques et Limites

    Conversions : Les données brutes (0-1023) sont converties en Lux (linéaire) et en dB (logarithmique via math.log10).

    Fiabilité : Utilisation du paramètre -u dans systemd pour un logging sans tampon et Restart=always en cas de crash.

    Limite : Le calcul des dB est une estimation logicielle sans étalonnage par sonomètre professionnel.