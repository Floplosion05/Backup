from meross_iot.manager import MerossManager
from meross_iot.meross_event import MerossEventType
from meross_iot.cloud.devices.power_plugs import GenericPlug
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from mqtt_publisher import publish_msg
import time
import threading
import socket
import json

REMOTE_SERVER = "www.google.com"
EMAIL = "surfandsail@gmx.de"
PASSWORD = "Ge1d0derLiebe"

plugs = []
devices = []
commands = ['0', '1', 'on', 'off', 'toggle', 'getinfo']
commands2 = ['getDevices']

def is_connected():
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

def event_handler(eventobj):
    if eventobj.event_type == MerossEventType.DEVICE_ONLINE_STATUS:
        print("Device online status changed: %s went %s" % (eventobj.device.name, eventobj.status))
        pass

    elif eventobj.event_type == MerossEventType.DEVICE_SWITCH_STATUS:
        print("Switch state changed: Device %s (channel %d) went %s" % (eventobj.device.name, eventobj.channel_id,
                                                                        eventobj.switch_state))
    elif eventobj.event_type == MerossEventType.CLIENT_CONNECTION:
        print("MQTT connection state changed: client went %s" % eventobj.status)

        # TODO: Give example of reconnection?

    elif eventobj.event_type == MerossEventType.GARAGE_DOOR_STATUS:
        print("Garage door is now %s" % eventobj.door_state)

    else:
        print("Unknown event!")

def execute(plug_name, command):
    
    if (plug_name != None):
        plug = manager.get_device_by_name(plug_name)

        if not plug.supports_electricity_reading():
            if plug.online:
                if command == '1' or command == 'on':
                    plug.turn_on()
                    
                elif command == '0' or command == 'off':
                    plug.turn_off()
                    
                elif command == 'toggle':
                    if (plug.get_status() == True):
                        plug.turn_off()
                    elif (plug.get_status() == False):
                        plug.turn_on()
                        
                elif command == 'getinfo':
                    print(str(plug.get_status()))
                    publish_msg("Hausautomation/" + plug_name, plug.get_status())
                    
            else:
                print('Device: ' + plug_name + ' seems to be offline')
                publish_msg("Hausautomation/" + plug_name, 'Offline')
        else:
            print('Device: ' + plug_name + ' suopports power cinsumption reading :P')
    else:
        if (command == 'getDevices'):
            print('Sending:')
            for plug in plugs:
                print(plug)
                publish_msg("Hausautomation/Meross", plug)
    
def subscribe(topic='Hausautomation', host='localhost', port=1883, keepalive=60):
    
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(topic)

    def on_message(client, userdata, msg):
        print(msg.topic + " " + msg.payload.decode())
        
        if msg.topic == topic:
            message_list = msg.payload.decode().split(' ')
            print(message_list)
            
            if (message_list[0] in plugs and message_list[1] in commands):
                print('Got plug: ' + message_list[0] + ' with command: ' + message_list[1])
                execute(message_list[0], message_list[1])
            
            elif (message_list[0] in commands2):
                print('Got command: ' + message_list[0])
                execute(None, message_list[0])
                
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port, keepalive)
    client.loop_forever()

while not is_connected():
    time.sleep(0.5)

manager = MerossManager.from_email_and_password(meross_email=EMAIL, meross_password=PASSWORD)

manager.register_event_handler(event_handler)

manager.start()

devices = manager.list_http_devices()

for d in devices:
    if d["onlineStatus"] == 1:
        plugs.append(d["devName"])
    else:
        print(d["devName"] + ' is offline')
print(plugs)

subscribe()
