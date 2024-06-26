import shutil
from PIL import Image
import cv2
import numpy as np

import base64
import os
import time
from datetime import datetime

import subprocess
import pygame

from openai import OpenAI

client = OpenAI(api_key="(API_KEY_HERE)")

MODEL = "gpt-4o"

audio_filename = "audiodescription.mp3"


# def play_mp3(file_path):
#    """
#    Play an MP3 file using afplay on macOS.
#
#    :param file_path: Path to the MP3 file
#    """
#    try:
#        subprocess.run(['afplay', file_path])
#    except FileNotFoundError:
#        print("afplay command not found. Make sure you're on macOS and afplay is installed.")

def play_mp3(file_path):
    # Initialize the mixer module in pygame
    pygame.mixer.init()

    # Load the mp3 file
    pygame.mixer.music.load(file_path)

    # Play the mp3 file
    pygame.mixer.music.play()

    # Let the music play in the background
    while pygame.mixer.music.get_busy():
        time.sleep(1)


def text_to_speech(text, filename):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    response.stream_to_file(filename)

def move_and_rename(filename):
    """
    Move and rename a single JPG file from one directory to another.

    :param filename: String, the path to the destination directory where the file should be moved with the new name.
    """
    # List all the files .jpg in the origin path
    files = [f for f in os.listdir("./data/Screenshots") if f.endswith('.jpg')]

    # Check if there is just one file
    if len(files) != 1:
        raise ValueError("There should be exactly one JPG file in the source directory.")
    
    # Make the complete path from the original path
    original_file_path = os.path.join("./data/Screenshots", files[0])


    # Move and rename the file
    shutil.move(original_file_path, filename)


def convert_image_to_base64(filepath):
    """
    Open an image from a filepath, then convert it to a base64 encoded string.

    :param filepath: String path to the image file
    :return: Base64 encoded string of the image
    """
    # load the imagem from the path
    cv2_image = cv2.imread(filepath)

    # Verify if the image was load
    if cv2_image is None:
        raise ValueError("Image not found or the format is not supported.")

    # Encode the image to a buffer in PNG format
    _, buffer = cv2.imencode('.png', cv2_image)

    # Convert the buffer to a base64 string
    base64_string = base64.b64encode(buffer).decode('utf-8')

    return base64_string

def capture_screenshot():
    """
    Capture a screenshot using ADB commands to set properties and capture an image from Meta Quest 3.

    :return: Combined output from the commands or an error message
    """
    try:
        # Properties of the print
        crop_command = "adb shell setprop debug.oculus.screenCaptureEye 1 && " \
                       "adb shell setprop debug.oculus.capture.width 1920 && " \
                       "adb shell setprop debug.oculus.capture.height 1080"

        # Execute the command for image configuration
        result1 = subprocess.run(crop_command, shell=True, text=True, check=True)

        # Print the image
        print_command = "adb shell am startservice -n com.oculus.metacam/.capture.CaptureService -a TAKE_SCREENSHOT"
        
        # Transfer the imagem from the oculus to the computer
        transfer_command = "adb pull /sdcard/Oculus/Screenshots/ ./data/ && " \
                           "adb shell rm /sdcard/Oculus/Screenshots/*.jpg"

        # Execute the print command
        result2 = subprocess.run(print_command, shell=True, text=True, capture_output=True, check=True)
        
        time.sleep(0.5)
        
        result3 = subprocess.run(transfer_command, shell=True, text=True, check=True)

        return result1.stdout

    except subprocess.CalledProcessError as e:
        return f"Error trying to execute the adb command: {e}"

while True:
    print("\nMenu:")
    print("1. AudioDescription Base")
    print("2. AudioDescription Locomotion")
    print("3. AudioDescription Text")
    print("4. AudioDescription Person")
    print("5. Exit")

    # Wait a valid input
    while True:
        inputOption = input("Insert the option: ")
        numberOption = int(inputOption)
        if (1 <= numberOption <= 5):
            break
        print("Invalid option, try again!")
    
    
    # time for the user change the screen
    print("You have 3 seconds to change to the screen application...")
    #time.sleep(3)

    # Start counting the time
    startTime = time.perf_counter()

    # Generate a timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Exit option
    if inputOption == '5':
        break

    # guide to folder
    if inputOption == '1':
        descOption = "Base"
    elif inputOption == '2':
        descOption = "Locomotion"
    elif inputOption == '3':
        descOption = "Text"
    elif inputOption == '4':
        descOption = "Person"

    # Create filenames with the timestamp
    filenamej = f"data/{descOption}/{timestamp}.jpg"
    filenamet = f"data/{descOption}/{timestamp}.txt"
    filenamem = f"data/{descOption}/{timestamp}.mp3"

    # Capture the screenshot
    capture_screenshot()

    # Move and rename the file save in /data/Screenshots path
    move_and_rename(filenamej)

    # Convert the OpenCV image to a base64 encoded string
    base64_string = convert_image_to_base64(filenamej)

    # Time of printScreen, move, rename and conversion
    printScreenTime = time.perf_counter() - startTime

    if inputOption == '1':
        role = "You are a person that provides professional audio description services. Help me describe the images I show you in Brazilian portuguese."
        text = "Please describe this image. Do not start the phrase with 'A imagem '"

    elif inputOption == '2':
        role = "You are a person that provides professional audio description services for blind people. Help me describe the images I show you in Brazilian portuguese."
        text = "Please describe this image focusing in aiding locomotion for a blind person. I want to know if the way ahead is free for walking. Describe the scene to help me to walk with more confidence, knowing if there is any obstacle in front of me. Be brief, i want a short sentence telling me only the necessary to step foward.x'"

    elif inputOption == '3':
        role = "You are a person that provides professional audio description services. Help me describe the images I show you in Brazilian portuguese."
        text = "Please describe this image. Do not start the phrase with 'A imagem '. Read any text you find. focus only on text you can find."

    else:
        role = "You are a person that provides professional audio description services. Help me describe the images I show you in Brazilian portuguese."
        text = "Please describe this image. Do not start the phrase with 'A imagem '. Describe the person in the center of the image. Focus on the facial features. Describe as gently as you can. I'm blind and want to know the person by her face."

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"{role}"},
            {"role": "user", "content": [
                {"type": "text", "text": f"{text}"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_string}"}
                 }
            ]}
        ],
        temperature=0.0,
    )

    text = response.choices[0].message.content

    # Time of sending and receiving data from GPT-4o
    responseTime = time.perf_counter() - startTime - printScreenTime

    print(text)

    with open(filenamet, 'w') as file:
        file.write(text)

    text_to_speech(text, filenamem)

    textToMP3Time = time.perf_counter() - startTime - printScreenTime - responseTime

    play_mp3(filenamem)

    # Time of the audio created
    audioTime = time.perf_counter() - startTime - printScreenTime - responseTime - textToMP3Time

    # Total time of the application
    totalTime = time.perf_counter() - startTime

    print(f"PrintScreen time: {printScreenTime}")
    print(f"Response from IA time: {responseTime}")
    print(f"Conversion text to MP3 time: {textToMP3Time}")
    print(f"Audio time: {audioTime}")
    print(f"Total Time: {totalTime}")