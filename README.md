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
- 1 . ```sudo apt install mosquitto mosquitto-clients python3 python3-pip rsync```

## Installation of the necessary scripts
- 1 .```mkdir /home/pi/Documents; mkdir /home/pi/autostart; mkdir /home/pi/Logs; cd /home/pi/Documents; git clone https://github.com/Floplosion05/Backup; cp -r Backup/* /home/pi/Documents; rm -r -f Backup/; cd /home/pi/Documents; rm -f README.md; cp autostart/* /home/pi/autostart; rm -r -f autostart/```

## (Optional) Setting up [SMB](https://pimylifeup.com/raspberry-pi-samba/)
- 1 . ```sudo apt install samba samba-common-bin```
- 2 .```mkdir /home/pi/shared```
- 3 .```sudo nano /etc/samba/smb.conf```
- 4 .At the bottom of the file add the lines:
```
[<<Your SMB folder's name>>]
path = /home/pi/shared
writeable=Yes
create mask=0777
directory mask=0777
public=no
```
- 5 .Save and exit, when using nano do so by hitting ```Crtl+X```, ```Y``` and ```Enter```
- 6 .Set a new Samba password by running ```sudo smbpasswd -a pi``` and then typing your new password
- 7 .Then restart Samba using ```sudo systemctl restart smbd```

## (optional) Setting up a Webserver with [Apache2](https://pimylifeup.com/raspberry-pi-apache/)
- 1 .```sudo apt install apache2 -y```
- 2 .Add write permissions to the user by running:
```
sudo usermod -a -G www-data pi
sudo chown -R -f www-data:www-data /var/www/html
```
- 3 .

## Installation of Python libraries via pip and git
- 1 . ```pip3 install paho-mqtt bs4 requests```
- 2 . ```git clone ```[```https://github.com/Floplosion05/MerossIot```](https://github.com/Floplosion05/MerossIot)
- 3 . ```cd MerossIot/```
- 4 . ```sudo python3 setup.py install```

## Creating a [Cronjob](https://www.raspberrypi.org/documentation/linux/usage/cron.md)
- 1 .```crontab -e```
     Normally You will be prompted to select your editor of choice, I just use nano and type ```1```
- 2 .At the bottom of the file add this line ```@reboot sh /home/pi/autostart/autostart.sh >/home/pi/Logs/cronlog.txt 2>&1```
- 3 .Save and exit, when using nano do so by hitting ```Crtl+X```, ```Y``` and ```Enter```
- 4 .You can check the cronjob by typing ```crontab -l```. This sjould return smething like this:
```
# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values fo
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command
@reboot sh /home/pi/autostart/autostart.sh >/home/pi/Logs/cronlog 2>&1

