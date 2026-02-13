# Protocole MQTT x Weather

## Payload des devices

- Format : **JSON**

- Payload :
	```json
	{
		MAC_ADDRESS: <value>,
		TIMESTAMP: <value>,
		METRICS: {
			LIGHT: <value>,
			SOUND: <value>,
			/* OR */
			TEMPERATURE: <value>,
			HUMIDITY: <value>,
		}
	}
	```

## Ports

- Phase de **TESTS**
	- Port au choix afin de pouvoir tester la réception de nos propres devices.
- Phase de **PRODUCTION**
	- **1883**, port par défaut pour MQTT, afin de receptionner tous les devices.

## Fréquence

- **Lumière et Son** : 
	- 10 secondes
	- car le volume du son et la lumière peuvent changer assez souvent au cours d'une période réduite.
- **DHT11 (Humidité et Température)** : 
	- 60 secondes,
	- car les températures et l'humidité ne changent pas aussi souvent que la lumière et le son.
- **Total** :
	- 7 réceptions par minutes
	- ce qui permet un débit très cocrect afin de recevoir de plusieurs appareils.

## QoS

- **Informations**
	- **Bande Passante** : 556x10³
	- **Taille d'un message type**: 992 bits x 2 = 1984 bits (multiplié par 2 pour prendre en compte les données MQTT)
	- **Niveaux de QoS** : 0 et 1


- **Duo d'appareils maximum interconnecté théorique**: $(556*10⁶)/(2*2*992)=140120$ **duo d'appareils**

- **Taux d'échecs** : Au vu de la marge que l'ont a sur la bande passante on fixe le taux d'echecs d'augmentation de la QoS à 5%.

- **Perte** : Afin de contrer des potentielles pertes lors d'un QoS à 1 nous ajoutons un accusé de reception.

