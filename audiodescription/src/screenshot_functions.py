import base64
import subprocess
import time
import cv2
import os
import shutil


def capture_screenshot():
    """
    Capture a screenshot using ADB commands to set properties and capture an image from Meta Quest 3.

    :parameter(s): None
    
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

        return f"result1: {result1.stdout}\nresult2: {result2.stdout}\nresult3: {result3.stdout}\n"

    except subprocess.CalledProcessError as e:
        return f"Error trying to execute the adb command: {e}"
    
def convert_image_to_base64(file_path):
    """
    Open an image from a filepath, then convert it to a base64 encoded string.

    :parameter(s):
        filepath: String path to the image file

    :return: Base64 encoded string of the image
    """
    # load the imagem from the path
    cv2_image = cv2.imread(file_path)

    # Verify if the image was load
    if cv2_image is None:
        raise ValueError("Image not found or the format is not supported.")

    # Encode the image to a buffer in PNG format
    _, buffer = cv2.imencode('.png', cv2_image)

    # Convert the buffer to a base64 string
    base64_string = base64.b64encode(buffer).decode('utf-8')

    return base64_string

def move_and_rename(file_path):
    """
    Move and rename a single JPG file from one directory to another.

    :parameter(s):
        file_path: String, the path to the destination directory where the file should be moved with the new name.
    
    :return: None
    """
    # List all the files .jpg in the origin path
    files = [f for f in os.listdir("./data/Screenshots") if f.endswith('.jpg')]

    # Check if there is just one file
    if len(files) != 1:
        raise ValueError("There should be exactly one JPG file in the source directory.")
    
    # Make the complete path from the original path
    original_file_path = os.path.join("./data/Screenshots", files[0])


    # Move and rename the file
    shutil.move(original_file_path, file_path)