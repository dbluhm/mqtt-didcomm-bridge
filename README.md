MQTT to DIDComm Bridge
======================

This is a very simple example of a DIDComm aware MQTT client.

Typically, IoT devices are incapable of participating in DIDComm due to lacking
the necessary crypto primitives on many devices (the ESP8266 family is a widely
used example of WiFi/Bluetooth capable but ECC incapable devices). A bridge
such as this one can be used to fill this gap.

The bridge retrieves the key and endpoint of the intended DIDComm recipient
from the environment, subscribes to all topics, then emits a DIDComm message for
each received message, with the payload and topic included in the message
contents.

Quickstart
----------

Requirements:
- Python 3.6 or higher
- A running MQTT broker

### Install
Create a python virtual environment and install dependencies:
```sh
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

Start the example receiver:
```sh
$ python receiver.py
```

And note the printed `verkey`.

Start the bridge:
```sh
$ MQTT_HOST="hostname" \
	THEIR_VK="<verkey from receiver>" \
	ENDPOINT="http://<receiver host>:<receiver port>" \
	python bridge.py
```
