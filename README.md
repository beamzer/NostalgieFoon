# NostalgieFoon
This python script is ment for a rotary phone with a Raspberry Pi Zero (can either be the Wireless version or without).
This is ment for elderly people because it brings back memories. By rotating the dial they will hear different tunes and music from the past.

## conversion process
Photo's below show how to modify a PTT W65 wall mounted rotary phone to work with the Raspberry Pi Zero.
Basically, pull it apart (gentely). Remove unnecessary components. Add the raspberry pi and connect the wires
to the Adafruit Speaker bonnet. These are large photo's, click on them to zoom in and view details.

![draaischijf](https://github.com/beamzer/PTT-Tafeltjes-Telefoon/blob/master/foto/img_2606.jpg)
![draaischijf](https://github.com/beamzer/PTT-Tafeltjes-Telefoon/blob/master/foto/img_2607.jpg)
![draaischijf](https://github.com/beamzer/PTT-Tafeltjes-Telefoon/blob/master/foto/img_2608.jpg)
![draaischijf](https://github.com/beamzer/PTT-Tafeltjes-Telefoon/blob/master/foto/img_2609.jpg)
![draaischijf](https://github.com/beamzer/PTT-Tafeltjes-Telefoon/blob/master/foto/img_2610.jpg)
![draaischijf](https://github.com/beamzer/PTT-Tafeltjes-Telefoon/blob/master/foto/img_2623.jpg)
![draaischijf](https://github.com/beamzer/PTT-Tafeltjes-Telefoon/blob/master/foto/img_2624.jpg)
![draaischijf](https://github.com/beamzer/PTT-Tafeltjes-Telefoon/blob/master/foto/img_0844.gif)

## Connections
For W65 (this is basically a T65 rotary phone, but wall mounted) with the
ZeroPi and Adafruit SpeakerBonnet which uses GPIO 18, 19 and 21, see:
[SpeakerBonnet pinouts](https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/pinouts)

Connect the Right-Out channel to the horn speaker

* rotary dial (Red and Yellow) connect to GPIO 23
* the other contact to GND
* a rotary dial is basically a switch, which switches at a frequency of 10 events per second (10Hz)\
&nbsp;
* solder a 100 nF condensator parallel to the switch to prevent jitter
* white button (earth switch) to GPIO 25
* the other side of the earth switch should go to GND\
&nbsp;
* horn contact to GPIO 4 and the other connection of the switch to GND
* 100 nF condensator parallel to prevent jitter


## Software

* It's best to install Raspbian Lite and add Pygame which is needed to play sound from python:
```
sudo apt install python-pygame
```

## Links

* Original idea by: [https://github.com/tammojan](https://github.com/tammojan/sommentelefoon)
* and modified by: [https://github.com/ralphcrutzen](https://github.com/ralphcrutzen/PTT-Tafeltjes-Telefoon)
* [PTT schematics for T65 phones](https://dutchtelecom.files.wordpress.com/2016/05/ptt_schema_t65_toestellen_1974-1987.pdf)

