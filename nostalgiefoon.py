#!/usr/bin/env python
#
import RPi.GPIO as GPIO
import sys
import os
import time
import pygame

# ###################################################################################
# Nostalgie Foon
# 20180818 Ewald
# v0.75
# afgeleid van https://github.com/ralphcrutzen/PTT-Tafeltjes-Telefoon
#
# #### Hardware :
# W65 wandtelefoon met draaischijf
# Raspberry Pi Zero Wireless
# Adafruit Speaker Bonnet
#
# ###  Definities voor W65 (= T65 wandtoestel), nummers zijn GPIO nummers (geen pin-nummers)
#
# Voor W65 (T65 wandtoestel)
# ZeroPi met Adafruit SpeakerBonnet, deze gebruikt GPIO 18,19 en 21, zie:
# https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/pinouts
# Rechts-Uit sluit je dan aan op de hoornluidspreker
#
# draaischijf (Rood en Geel) aansluiten op SCHIJFPIN en de andere op GND
SCHIJFPIN = 23

# andere contact van AardSchakelaar verbinden met GND
# 100 nF condensator over het contact solderen om "denderen" tegen te gaan
AARDPIN = 25

# hoorncontact aansluiten zodat hoorn opnemen contact naar GND maakt
# 100 nF condensator over het contact solderen om "denderen" tegen te gaan
HOORNPIN = 4
#
#
# ####################################################################################

# VOL = 0.8           # Volume op 80%
first = True        # om alleen eerste keer welkomst boodschap te horen
asc = 0             # AardSchakelaar Counter
ast = 100           # AardSchakelaar Timer voor shutdown = 100 * 0.1s (10s)


def speel(bestand, VOL=0.8):
    pygame.mixer.music.load(bestand)
    pygame.mixer.music.set_volume(VOL)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


def speelMuziek(getal):
    print "Speel nummer", getal
    speel("/home/pi/PROJECT/audio/" + str(getal) + ".mp3")


def speelfolder(folder):
    files = []
    file_index = 0
    for filename in os.listdir("/home/pi/PROJECT/" + folder):
        if filename.endswith(".mp3", ".wav"):
            files.append(filename)
    files.sort()    # do this if you want them in name order

    while True:
        print "Speel " + folder + " " + files[file_index]
        speel("/home/pi/PROJECT/" + folder + "/" + files[file_index])
        file_index = (file_index + 1) % len(files)


def getNummer():
    nPulsen = 0
    t = 0
    wt = 2000                  # wait time = 200 * 0.1s (20s)

    print "Wacht op draaischijf.."

    schijfContact = GPIO.input(SCHIJFPIN)

    while not schijfContact:
        if t > wt:          # time-out routine
            t = 0
            return -1       # time-out!
        schijfContact = GPIO.input(SCHIJFPIN)
        t += 1
        time.sleep(0.01)

    # Afhandelen van pulsen
    klaar = False
    while not klaar and schijfContact:
        nPulsen = nPulsen + 1
        startTijd = time.time()
        time.sleep(0.1)
        schijfContact = GPIO.input(SCHIJFPIN)

        # Controleer tijd tussen twee pulsen
        while not klaar and not schijfContact:
            if time.time() - startTijd >= 0.2:
                klaar = True
            schijfContact = GPIO.input(SCHIJFPIN)

    return nPulsen % 10


def AardCallback(channel):
    print "AardSchakelaar gedrukt op GPIO ", channel
#    if GPIO.input(channel):
#        print " Rising edge"
#    else:
#        print " Falling edge"
    pygame.mixer.music.stop()


def hoornCallback(channel):
    print "Hoorn interrupt op GPIO ", channel
#    if GPIO.input(channel):
#        print " Rising edge"        # Hoorn van de haak
#    else:
#        print " Falling edge"       # Hoorn op de haak
#
# herstart het hele script
    GPIO.cleanup()
    python = sys.executable
    os.execl(python, python, * sys.argv)


# BCM numbering scheme (Broadcom SOC channel), dus getallen zijn GPIO nummers
GPIO.setmode(GPIO.BCM)
# alles pull-up, want contacten schakelen naar GND
GPIO.setup(SCHIJFPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(HOORNPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(AARDPIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Gebruik een interrupt voor de hoorn,
# omdat deze op elk moment kan worden neergelegd
GPIO.add_event_detect(HOORNPIN, GPIO.BOTH, callback=hoornCallback)

GPIO.add_event_detect(AARDPIN, GPIO.FALLING, callback=AardCallback)

pygame.mixer.init()

while True:		# main program loop
    try:
        print "Start"
        hoornContact = GPIO.input(HOORNPIN)
        if not hoornContact:
            first = True

        while not hoornContact:            # zolang hoorn op de haak ligt
            hoornContact = GPIO.input(HOORNPIN)
            aardContact = GPIO.input(AARDPIN)
            if not aardContact:
                asc += 1
                if asc > ast:
                    print "shutdown"
                    speel("/home/pi/PROJECT/audio/CarHorn.mp3", 1)
                    asc = 0
                    from subprocess import call
                    call("sudo shutdown -h now", shell=True)
            else:
                asc = 0
            time.sleep(0.1)

        if first is True:                       # speel een keer na opnemen hoorn
            print "leuk dat je belt"
            speel("/home/pi/PROJECT/audio/leuk_dat_je_belt.mp3")
            first = False

        time.sleep(0.5)
        print "draai een nummer"
        speel("/home/pi/PROJECT/audio/draai_een_nummer.mp3")

        mp3nr = getNummer()
        print "gekozen voor: %d" % mp3nr
        speel("/home/pi/PROJECT/nummers/" + str(mp3nr) + ".mp3")

        time.sleep(1)

        if mp3nr == -1:         # time-out
            speelfolder("AndreRieu")
        if mp3nr == 8:
            speelfolder("Bingo")
        if mp3nr == 9:
            speelfolder("AndreRieu")
        if mp3nr == 0:
            speelfolder("Reclame")
        else:
            speelMuziek(mp3nr)

    except KeyboardInterrupt:          # Ctrl+C
        print ""
        print "CTRL-C, byebye..."
        GPIO.cleanup()
        sys.exit(0)
