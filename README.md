# Backup
## Preparation
 - 1 . Download [Raspberry Pi Imager](https://downloads.raspberrypi.org/imager/imager_1.4.exe) and install Raspbian OS with it on an sd card
 - 2 . Add an empty file called ssh with no extension in the root directory of the new flashed sd card
 - 3 . If using a Wifi connection add a file called [```wpa_supplicant.conf```](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) containing:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<<Insert 2 letter ISO 3166-1 country code here>>

network={
 ssid="<<Name of your wireless LAN>>"
 psk="<<Password for your wireless LAN>>"
}
```
otherwise just plug in your ethernet cable
 - 4 . 
