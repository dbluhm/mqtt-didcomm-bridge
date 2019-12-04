import asyncio
import os
import signal
import time

from gmqtt import Client as MQTTClient
from aries_staticagent import StaticConnection, crypto


STOP = asyncio.Event()

class DIDCommTeeMQTTClient:
    def __init__(self, their_vk, endpoint):
        self.client = MQTTClient("client-id")

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe

        self.did_conn = StaticConnection(
            crypto.create_keypair(),
            their_vk=their_vk,
            endpoint=endpoint
        )

    async def mqtt_connect(self, broker_host):
        await self.client.connect(broker_host)

    async def mqtt_disconnect(self):
        await self.client.disconnect()

    def on_connect(self, client, flags, rc, properties):
        print('Connected')

    async def on_message(self, client, topic, payload, qos, properties):
        await self.did_conn.send_async({
            '@type': 'https://didcomm.dbluhm.com/mqtt/0.1/msg',
            'topic': topic,
            'payload': payload.decode('ascii'),
            'properties': properties
        })
        print('RECV MSG:', payload)

    def on_disconnect(self, client, packet, exc=None):
        print('Disconnected')

    def on_subscribe(self, client, mid, qos):
        print('SUBSCRIBED')

    def publish(self, *args, **kwargs):
        self.client.publish(*args, **kwargs)

    def subscribe(self, *args, **kwargs):
        self.client.subscribe(*args, **kwargs)


async def main(broker_host, their_vk, endpoint):
    client = DIDCommTeeMQTTClient(their_vk, endpoint)
    await client.mqtt_connect(broker_host)
    await client.did_conn.send_async({
        '@type': 'https://didcomm.dbluhm.com/mqtt/0.1/connected'
    })
    client.subscribe('#', qos=0)
    await client.did_conn.send_async({
        '@type': 'https://didcomm.dbluhm.com/mqtt/0.1/subscribed',
        'topic': '#'
    })

    client.publish('TEST/TIME', str(time.time()), qos=1)

    await STOP.wait()
    await client.mqtt_disconnect()
    await client.did_conn.send_async({
        '@type': 'https://didcomm.dbluhm.com/mqtt/0.1/disconnected'
    })


def ask_stop():
    STOP.set()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, ask_stop)
    loop.add_signal_handler(signal.SIGTERM, ask_stop)

    host = os.environ.get('MQTT_HOST')
    their_vk = os.environ.get('THEIR_VK')
    endpoint = os.environ.get('ENDPOINT')

    loop.run_until_complete(main(host, their_vk, endpoint))
