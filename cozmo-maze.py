import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import sys
import os
import shutil
import requests
import json
import time
import asyncio
import datetime
import socket
import time
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 9999))
sock.listen(1)
conn, addr = sock.accept()
print("connected:", addr)

isProcessing = False
isTakingPicture = False
puppyFound = False
totoFound = False
minionFound = False
puppyHello = False
totoHello = False
minionHello = False

def parseResponse(response):
    print(f"response is {response}")
    global puppyFound
    global totoFound
    global minionFound
    entries = {}
    highestConfidence = 0.0
    highestEntry = ''
    print(response)
    for key in response.keys():
        if key == "answer":
            for guess in response[key].keys():
                print(f"guess: {guess}")
                entries[response[key][guess]] = guess
    for key in entries.keys():
        if key > highestConfidence:
            highestConfidence = key
            highestEntry = entries[key]
    if highestConfidence > 0.8:
        if highestEntry == "puppy":
            puppyFound = True
        if highestEntry == "minion":
            minionFound = True
        if highestEntry == "toto":
            totoFound = True


def on_new_camera_image(evt, **kwargs):
    global isProcessing
    global isTakingPicture

   if isTakingPicture:
        if not isProcessing:
            isProcessing = True
            pilImage = kwargs['image'].raw_image
            photo_filename = f"fromcozmo-{kwargs['image'].image_number}.jpeg"
            photo_location = f"/tmp/objects/photos/fromcozmo-{kwargs['image'].image_number}.jpeg"
            print(f"photo_location is {photo_location}")
            pilImage.save(photo_location, "JPEG")
            image_cmd = f"Image:{photo_filename}\n"
            conn.send(image_cmd.encode())
            time.sleep(1)
            isProcessing = False

def hello(robot):
    global puppyFound
    global totoFound
    global minionFound
    global puppyHello
    global totoHello
    global minionHello
    if totoFound:
        if not totoHello:
            robot.say_text(f"I've found Toto. Hello Toto!").wait_for_completed()
            helloToto = True
    if minionFound:
        if not minionFound:
            robot.say_text(f"I've found Minion. Hello Minion!").wait_for_completed()
            helloMinion = True
    if puppyFound:
        if not puppyHello:
            robot.say_text(f"I've found Puppy. Hello Puppy!").wait_for_completed()
            puppyHello = True

def straight(robot, distance):
    global isTakingPicture
    isTakingPicture = False
    hello(robot)
    robot.drive_straight(distance_mm(distance), speed_mmps(50)).wait_for_completed()
    isTakingPicture = False

def turn(robot, angle):
    global isTakingPicture
    isTakingPicture = False
    hello(robot)
    robot.turn_in_place(degrees(angle)).wait_for_completed()
    isTakingPicture = True
    time.sleep(1)

def cozmo_program(robot: cozmo.robot.Robot):
    global isTakingPicture

    robot.set_head_angle(degrees(10.0)).wait_for_completed()
    robot.set_lift_height(0.0).wait_for_completed()
    robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image)

    straight(robot, 130)
    conn.send("Location:130,0\n".encode())

    turn(robot, -90)

cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
