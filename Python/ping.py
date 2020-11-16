import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading
import requests

MQTT_SERVER = "192.168.100.98"


def send_message():
    requests.get('https://maker.ifttt.com/trigger//with/key/b-l-V06AbzAM4E9Iv2aEn7NGMk6ZCr4dVaCETS_WV1a')

def subscribe(topic='002', host='localhost', port=1883, keepalive=60):
    
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(topic)

    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        
        if msg.topic == '002':
            if msg.payload == b'pinghost':
                publish.single('002', 'pingclient', hostname=MQTT_SERVER)
                timer.cancel()
                timer.start()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port, keepalive)
    client.loop_forever()
        
timer = threading.Timer(400, send_message)
timer.start()
subscribe()

    
