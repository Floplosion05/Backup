# Backup
Wherever there is something ```<<encapsulated>>``` you have to fill in your own credentials.
## Preparation
 - 1 . Download [Raspberry Pi Imager](https://downloads.raspberrypi.org/imager/imager_1.4.exe) and install Raspbian OS with it on an sd card
 - 2 . Add an empty file called ssh with no extension in the root directory of the new flashed sd card
 - 3 . If using an Ethernet connection just plug in your sd card and LAN cable and your good to go; If you are using a Wifi connection add a file called [```wpa_supplicant.conf```](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) containing the following and proceed with the mentioned steps
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<<Insert 2 letter ISO 3166-1 country code here>>

network={
 ssid="<<Name of your wireless LAN>>"
 psk="<<Password for your wireless LAN>>"
}
```
 - 4 . Get the Ip of your raspberrypi via your router
 - 5 . Open cmd and enter ```ssh pi@<<your raspberrypi's ip>>``` and when asked to type the default password ```raspberry```
 - 6 . As soon as your connected to the pi via ssh enter ```passwd``` and change the default password
 - 7 . Run ```sudo get update``` and ```sudo get upgrade```
 - 8 . Run ```sudo raspi-config``` go to ```System Options(1)``` and then to ```Network at boot(S6)``` and confirm by choosing ```yes``` then leave the config by selecting ```Finish```

## Installation of linux packages via apt
- 1 . ```sudo apt install mosquitto mosquitto-clients python3 python3-pip```
- 2 . ``````
## (Optional) Setting up SMB
- 1 . 

## (optional) Setting up a Webserver with Apache2

## Installation of Python libraries via pip and git
- 1 . ```pip3 install paho-mqtt bs4 requests```
- 2 . ```git clone ```[```https://github.com/Floplosion05/MerossIot```](https://github.com/Floplosion05/MerossIot)
- 3 . ```cd MerossIot/```
- 4 . ```sudo python3 setup.py install```

## Installation of the necessary scripts
