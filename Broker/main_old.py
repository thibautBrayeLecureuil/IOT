import json
import paho.mqtt.client as mqtt

#Configuration du config.json
with open("config.json", "r") as f:
    data = json.load(f)

#Juste des variables
broker = data['mqtt']['broker']
port = data['mqtt']['port']
topics = data['mqtt']['topics']
acktopic = data['mqtt']['ack_topic']

def on_connect(client, userdata, flags, rc):
    for topic in topics:
        client.subscribe(topic) #On s'abonne aux topics
        print(f"abonné à : {topic}")

def on_message(client, userdata, msg):
    try:
        payload_str = json.loads(msg.payload.decode("utf-8")) #On déchiffre le message reçu
        mac_source = payload_str.get("MAC_ADDRESS")
        metrics = payload_str.get('METRICS')
        #print(f"Message reçu de {mac_source} sur {msg.topic} :")
        #print(f"Données : {metrics}")
        if "TEMPERATURE" in metrics:
            var_temp.set(f"Température : {metrics['TEMPERAURE']}")

        #Preparation du message d'acquittement
        ack_payload = json.dumps({
            "target_mac": mac_source,
            "status": "OK",
            "timestamp": payload_str.get("TIMESTAMP")
        })

        #Envoie de l'aquittement
        client.publish(acktopic, ack_payload)
        print(f"ACK envoyé vers {acktopic}")
    except Exception as e:
        print(f"Erreur : {e}")    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(broker, port, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print("\nArrêt de la supervision.")
