import pyautogui
import pygame
from PIL import Image
import cv2
import numpy as np

import base64
import os
import ssl
import time
from datetime import datetime

import subprocess

from openai import OpenAI

client = OpenAI(api_key="(API_KEY)")

MODEL="gpt-4o"

audio_filename = "audiodescription.mp3"

time.sleep(1)

import subprocess

def play_mp3(file_path):
    # Initialize the mixer module in pygame
    pygame.mixer.init()

    # Load the mp3 file
    pygame.mixer.music.load(file_path)

    # Play the mp3 file
    pygame.mixer.music.play()

    # Let the music play in the background
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

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

    # Generate a timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Create filenames with the timestamp
    filenamej = f"data/{timestamp}.jpg"
    filenamet = f"data/{timestamp}.txt"
    filenamem = f"data/{timestamp}.mp3"

    # Capture the screenshot
    pil_screenshot = capture_screenshot()

    # Convert the PIL screenshot to an OpenCV image
    cv2_screenshot = pil_to_cv2(pil_screenshot)

    # Crop the OpenCV image to the biggest square region in the middle
    cropped_image = crop_to_square(cv2_screenshot)

    cv2.imwrite(filenamej, cropped_image)

    # Convert the OpenCV image to a base64 encoded string
    base64_string = convert_cv2_to_base64(cropped_image)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a person that provides professional audio description services. Help me describe the images I show you in Brazilian portuguese."},
            {"role": "user", "content": [
            {"type": "text", "text": "Please describe this image. Do not start the phrase with 'A imagem '"},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_string}"}
                }
            ]}
        ],
        temperature=0.0,
        )

    text = response.choices[0].message.content

    print(text)

    with open(filenamet, 'w') as file:
        file.write(text)

    text_to_speech(text, filenamem)

    play_mp3(filenamem)

# Display the cropped image using OpenCV
#cv2.imshow('Cropped Screenshot', cropped_image)
#cv2.waitKey(1)  # Wait for a key press to close the window
#cv2.destroyAllWindows()  # Close the window
