#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
#    Base on Daniel Perron and Mario Gomez <mario.gomez@teubi.co>   MFRC522-Python
#
#    This file use part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software:
#    you can redistribute it and/or modify
#    it under the terms of
#    the GNU Lesser General Public License as published by the
#    Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the
#    GNU Lesser General Public License along with MFRC522-Python.
#    If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import MFRC522
import signal
import requests

# Load environment variables
import os
from dotenv import load_dotenv
load_dotenv("params.env")
# Get server IP
SERVER_IP = os.getenv("SERVER_IP")

continue_reading = True


# function to read uid an conver it to a string

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = format(i, '02X') + mystring
    return mystring


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

# This loop keeps checking for chips.
# If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # print(status)
    # print(TagType)
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_SelectTagSN()
        # If we have the UID, continue
        uid_str = uidToString(uid)
        if status == MIFAREReader.MI_OK:
            print("Card read UID: %s" % uid_str)
            req = requests.post(url=f"http://{SERVER_IP}/", json={"uid_str" : uid_str}, headers={"Content-Type":"application/json"})
            print(req.text)
        else:
            print("Authentication error")

