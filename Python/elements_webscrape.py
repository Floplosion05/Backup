#//Imports//
import requests
from bs4 import BeautifulSoup
from mqtt_publisher import publish_msg
import socket
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

#//Vars//
REMOTE_SERVER = "www.google.com"
URL = 'https://www.elements.com/auslastung/?set_studio=elements-eschborn'
COMMANDS = ['getCount']
TOPICS = ['Hausautomation/Elements']

#//Funcs//
def is_connected():
	try:
		host = socket.gethostbyname(REMOTE_SERVER)
		s = socket.create_connection((host, 80), 2)
		return True
	except:
		pass
	return False

def refresh_page():
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, 'html.parser')
	result = int(soup.find("div", class_="checkin-number").text.replace("\n","").split("/",1)[0])
	return result

def subscribe(topic='Hausautomation/#', host='localhost', port=1883, keepalive=60):
	
	def on_connect(client, userdata, flags, rc):
		print("Conne4cted with result code "+str(rc))
		client.subscribe(topic)

	def on_message(client, userdata, msg):
		
		if msg.topic in TOPICS:
			message = msg.payload.decode()
			print(msg.topic + ' : ' + message)
			if (message in COMMANDS):
				print('Got Command: ' + message)
				publish_msg('Hausautomation/Elements', refresh_page())

				
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
