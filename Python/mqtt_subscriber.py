import paho.mqtt.client as mqtt
import time

def subscribe(topic='006', host='localhost', port=1883, keepalive=60):
    
    
    def on_connect(client, userdata, flags, rc):
        #print("Connected with result code " + str(rc))
        client.subscribe(topic)

    def on_message(client, userdata, msg):
        print(msg.topic + " " + msg.payload.decode())
    
    print(topic + ':' + host + ':' + str(port) + ':' + str(keepalive))
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port, keepalive)
    client.loop_forever()

subscribe()
