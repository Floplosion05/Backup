import paho.mqtt.publish as publish

MQTT_SERVER = "localhost"

def publish_msg(topic="002", message="lol"):
	publish.single(topic, message, hostname=MQTT_SERVER)
