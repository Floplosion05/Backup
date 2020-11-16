import json
from mqtt_publisher import publish_msg
import socket
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time

TOPIC = 'Hausautomation/ir_server'
REMOTE_SERVER = "www.google.com"

with open('beamer.json', 'r') as f:
	data = json.load(f)

def is_connected():
	try:
		host = socket.gethostbyname(REMOTE_SERVER)
		s = socket.create_connection((host, 80), 2)
		return True
	except:
		pass
	return False

def subscribe(topic='Hausautomation/#', host='localhost', port=1883, keepalive=60):
	
	def on_connect(client, userdata, flags, rc):
		print("Conne4cted with result code "+str(rc))
		client.subscribe(topic)

	def on_message(client, userdata, msg):
		
		if msg.topic in TOPIC:
			message = msg.payload.decode()
			if (message in data):
				print(msg.topic + ' : ' + message)
				print('Code: ' + data[message][0])
				if len(data[message]) == 1:
					publish_msg('ir_server/send', data[message][0])
				else:
					for command in data[message]:
						publish_msg('ir_server/send', command)
						time.sleep(0.5)

				
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	client.connect(host, port, keepalive)
	client.loop_forever()

if __name__ == '__main__':
	while not is_connected():
		time.sleep(1)
	else:
		subscribe()
