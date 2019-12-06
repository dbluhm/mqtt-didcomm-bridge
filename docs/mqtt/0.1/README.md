MQTT Protocol Message Definitions
=================================

## Notification Messages

The following messages are sent as notifications of events.

### Msg

Sent when a topic the bridge is subscribed to is published.

Example:
```json
{
    "@type": "https://didcomm.dbluhm.com/mqtt/0.1/msg",
    "topic": "test/topic",
    "payload": "test payload",
    "properties": {
        ...
    }
}
```

### Connected

Sent on connection established to MQTT broker.

Example:
```json
{
    "@type": "https://didcomm.dbluhm.com/mqtt/0.1/connected",
    "broker": "<hostname of MQTT broker>"
}
```

### Disconnected

Sent on connection closed.

Example:
```json
{
    "@type": "https://didcomm.dbluhm.com/mqtt/0.1/disconnected"
}
```

### Subscribed

Sent on new subscription.

Example:
```json
{
    "@type": "https://didcomm.dbluhm.com/mqtt/0.1/subscribed",
    "topic": "#"
}
```

## Commands

The following messages are sent as commands to the MQTT bridge.

> **_Note:_** The bridge currently doesn't support these.

### Publish

Instruct the bridge to publish a message to a topic.

Example:
```json
{
    "@type": "https://didcomm.dbluhm.com/mqtt/0.1/publish",
    "topic": "test/topic",
    "payload": "test payload",
    "qos": 0
}
```

### Subscribe

Instruct the bridge to subscribe to a new topic.

Example:
```json
{
    "@type": "https://didcomm.dbluhm.com/mqtt/0.1/subscribe",
    "topic": "test/topic"
}
```
