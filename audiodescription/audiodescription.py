import pyautogui
from PIL import Image
import cv2
import numpy as np

import base64
import os
import ssl
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


def convert_cv2_to_base64(cv2_image):
    """
    Convert an OpenCV image to a base64 encoded string.

    :param cv2_image: OpenCV Image (numpy array)
    :return: Base64 encoded string of the image
    """
    # Encode the image to a buffer
    _, buffer = cv2.imencode('.png', cv2_image)

    # Convert the buffer to a base64 string
    base64_string = base64.b64encode(buffer).decode('utf-8')

    return base64_string


def pil_to_cv2(pil_image):
    """
    Convert a PIL Image to an OpenCV image (numpy array).

    :param pil_image: PIL Image object
    :return: OpenCV Image (numpy array)
    """
    open_cv_image = np.array(pil_image)
    # Convert RGB to BGR
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
    return open_cv_image


def capture_screenshot():
    """
    Capture a screenshot using pyautogui.

    :return: PIL Image object of the screenshot
    """
    screenshot = pyautogui.screenshot()
    return screenshot


def crop_to_square(image):
    """
    Crop the image to the biggest square region in the middle.

    :param image: OpenCV Image (numpy array)
    :return: Cropped OpenCV Image (numpy array)
    """
    height, width, _ = image.shape
    min_dim = min(height, width)
    start_x = width // 2 - min_dim // 2
    start_y = height // 2 - min_dim // 2
    cropped_image = image[start_y:start_y + min_dim, start_x:start_x + min_dim]
    return cropped_image


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
    time.sleep(3)

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
    pil_screenshot = capture_screenshot()

    # Convert the PIL screenshot to an OpenCV image
    cv2_screenshot = pil_to_cv2(pil_screenshot)

    # Crop the OpenCV image to the biggest square region in the middle
    cropped_image = crop_to_square(cv2_screenshot)

    cv2.imwrite(filenamej, cropped_image)

    # Convert the OpenCV image to a base64 encoded string
    base64_string = convert_cv2_to_base64(cropped_image)

    # Time of printScreen, crop and conversion
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

# Display the cropped image using OpenCV
# cv2.imshow('Cropped Screenshot', cropped_image)
# cv2.waitKey(1)  # Wait for a key press to close the window
# cv2.destroyAllWindows()  # Close the window
