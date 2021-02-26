# Backup
Wherever there is something ```<<encapsulated>>``` you have to fill in your own credentials.

## Preparation
 - Download [Raspberry Pi Imager](https://downloads.raspberrypi.org/imager/imager_1.4.exe) and install Raspberrypi OS **Lite** 32-Bit with it on a SD card (Navigate to Raspberry Pi OS (other))
 - Add an empty file named "ssh" **without** an extension in the root directory of the newly flashed SD card
 - If you are using an Ethernet connection:
   - just plug in your sd card and LAN cable and you're good to go
 - If you are using a Wifi connection:
   - add a file called [```wpa_supplicant.conf```](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md) containing the following and proceed with the mentioned steps
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<<Insert 2 letter ISO 3166-1 country code here>>

network={
 ssid="<<Name of your wireless LAN>>"
 psk="<<Password for your wireless LAN>>"
}
```
 After powering the unit, give it some time to boot up
- Get the IP of your raspberry Pi via your router (Usually the hostname is raspberry)
- Open Cmd and enter ```ssh pi@<<Your Pi's IP>>``` and when prompted provide the default password ```raspberry```
- Once connected to the Pi via ssh, enter ```passwd``` and change the default password
- Run ```sudo apt-get update``` and ```sudo apt-get upgrade```
- Next run ```sudo raspi-config``` go to ```System Options(1) or Boot Options(3)``` and then to ```Network at Boot(S6) or Wait for Network at Boot(B2)``` and confirm by choosing ```yes```, then go to ```System Options(1) or Network Options(2)``` followed by ```Hostname(S4) or Hostname(N1)```, then choose a different hostname than your primary node's (eg ```raspberrypi2```) and exit the configuration by selecting ```Finish```. Normally you will be asked if you want to reboot, hit ```YES```

## Configuring [SSH](https://serverpilot.io/docs/how-to-use-ssh-public-key-authentication/)
- Run ```ssh-keygen``` and confirm the next 3 questions with ```Enter```
- Next run this command with the IP of the target Pi ```ssh-copy-id pi@<<PRIMARY NODE'S IP>>``` and enter the password for the target Pi when asked

To test the configured ssh connection just type ```ssh pi@<<PRIMARY NODE'S IP>>``` and use the same IP as before, you should be able to log into the pi without entering your password.
This is later needed for smooth file-syncing

## Installation of linux packages via apt
- ```sudo apt install mosquitto mosquitto-clients python3 python3-pip rsync git```

## Configuring the MQTT-Broker
- ```sudo systemctl enable mosquitto.service```
- ```sudo systemctl start mosquitto.service```

## Installation of the necessary scripts
- ```mkdir /home/pi/Documents; mkdir /home/pi/autostart; mkdir /home/pi/Logs; cd /home/pi/Documents; git clone https://github.com/Floplosion05/Backup; cp -r Backup/* /home/pi/Documents; rm -r -f Backup/; cd /home/pi/Documents; rm -f README.md; cp autostart/* /home/pi/autostart; rm -r -f autostart/```
- Don't forget to change the meross cloud credentials in line [14, 15](https://github.com/Floplosion05/Backup/blob/main/Python/arduino2meross.py#L14) of the arduino2meross.py file (eg. typing ```nano /home/pi/Documents/Python/arduino2meross.py```)
- Don't forget to change your url to be called in line [7](https://github.com/Floplosion05/Backup/blob/main/Python/ping.py#L7) of the ping.py file

## (Optional) Setting up [SMB](https://pimylifeup.com/raspberry-pi-samba/)
- ```sudo apt install samba samba-common-bin```
- ```mkdir /home/pi/shared```
- ```sudo nano /etc/samba/smb.conf```
- At the bottom of the file add the lines:
```
[<<Your SMB folder's name>>]
path = /home/pi/shared
writeable=Yes
create mask=0777
directory mask=0777
public=no
```
- Save and exit, when using nano do so by hitting ```Crtl+X```, ```Y``` and ```Enter```
- Set a new Samba password by running ```sudo smbpasswd -a pi``` and then typing your new password
- Restart Samba using ```sudo systemctl restart smbd```

## (Optional) Setting up a Webserver with [Apache2](https://pimylifeup.com/raspberry-pi-apache/)
- ```sudo apt install apache2 -y```
- Add write permissions to the user by running:
```
sudo usermod -a -G www-data pi
sudo chown -R -f www-data:www-data /var/www/html
```
- Then type ```sudo nano /etc/apache2/apache2.conf``` and find the lines (usually starts on line 170:
```
<Directory /var/www/>
  Options Indexes FollowSymLinks
  AllowOverride None
  Require all granted
</Directory>
```
and change it to:
```
<Directory /var/www/>
  Options FollowSymLinks
  AllowOverride None
  Require all granted
</Directory>
```
Save and exit
- Then type ```sudo cp -r /home/pi/Documents/Shelly/* /var/www/html/```
- Finally enter ```systemctl restart apache2.service```

## Installation of Python libraries via pip and git
- ```pip3 install paho-mqtt bs4 requests```
- ```cd /home/pi/Documents/; git clone ```[```https://github.com/Floplosion05/MerossIot```](https://github.com/Floplosion05/MerossIot)
- ```cd MerossIot/```
- ```sudo python3 setup.py install```

## Creating a [Cronjob](https://www.raspberrypi.org/documentation/linux/usage/cron.md)
- ```crontab -e```
     Normally you will be prompted to select your editor of choice, I just use nano and type ```1```
- At the bottom of the file add these lines:
```
@reboot sh /home/pi/autostart/autostart.sh >/home/pi/Logs/cronlog.txt 2>&1
0 0 * * * rsync -avhp -e ssh pi@<<PRIMARY NODE'S IP>>:/home/pi/.node-red/flows.json /home/pi/.node-red/flows.json >/home/pi/Logs/rsynclog.txt 2>&1 && sudo systemctl restart nodered
```
- Save and exit, when using nano do so by hitting ```Crtl+X```, ```Y``` and ```Enter```
- You can check the cronjob by typing ```crontab -l```. This should return smething like this:
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
@reboot sh /home/pi/autostart/autostart.sh >/home/pi/Logs/cronlog.txt 2>&1
0 0 * * * rsync -avhp -e ssh pi@<<PRIMARY NODE'S IP>>:/home/pi/.node-red/flows.json /home/pi/.node-red/flows.json >/home/pi/Logs/rsynclog.txt 2>&1 && sudo systemctl restart nodered
```
## Setting up Node-Red
- Run ```bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)``` and confirm the following two questions with y for yes
- ```sudo systemctl enable nodered.service```
- ```cp -f -r /home/pi/Documents/NodeRed/* /home/pi/.node-red/;```
- ```sudo systemctl start nodered.service```
- Then point your browser at the Ip Adress of your pi and add the port: ```http://<<Your Pi's IP>>:1880``` to test the installation
- Next click on the three horizontal lines in the top right corner and go to ```Manage palette```, then install each of these nodes:
```
node-red-contrib-counter
node-red-contrib-cpu
node-red-contrib-device-stats
node-red-contrib-googlehome
node-red-contrib-google-oauth-calendar
node-red-contrib-hs100
node-red-contrib-moment
node-red-contrib-presence-faker
node-red-contrib-ui-level
node-red-contrib-viera
node-red-contrib-volumio
node-red-dashboard
node-red-node-openweathermap
node-red-node-suncalc
node-red-node-ui-list
```
- Type ```sudo systemctl stop nodered```
- Run ```rsync -avhp -e ssh pi@<<PRIMARY NODE'S IP>>:/home/pi/.node-red/flows.json /home/pi/.node-red/flows.json; sudo systemctl restart nodered```
- Using [enviroment variables](https://stackoverflow.com/questions/44298263/is-it-possible-to-declare-global-variables-in-node-red-and-use-them-on-the-node) in Node-Red
