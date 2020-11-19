import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import threading
import requests

def send_message():
    print('Client unreachable')
    requests.get(<<YOUR URL HERE>>)

def subscribe(topic='002', host='localhost', port=1883, keepalive=60):
    
    global timer
    
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(topic)

    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        
        if msg.topic == '002':
            if msg.payload == b'pinghost':
                publish.single('002', 'pingclient', hostname='localhost')
                timer.cancel()
                timer = threading.Timer(400, send_message)
                timer.start()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port, keepalive)
    client.loop_forever()
        
timer = threading.Timer(400, send_message)
timer.start()
subscribe()

    
