import time
from datetime import datetime


from src import parameters_functions as parameters
from src import audio_functions as audio
from src import screenshot_functions as screenshot

from openai import OpenAI

with open("Api_key.txt", 'r') as file:
    api_key_file = file.read()

client = OpenAI(api_key=api_key_file)

MODEL = "gpt-4o"    

audio.boot_start()

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
    
    # Start counting the time
    startTime = time.perf_counter()

    # Generate a timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Exit option
    if inputOption == '5':
        break

    # guide to folder
    if inputOption == '1':
        descOption = "base"
    elif inputOption == '2':
        descOption = "locomotion"
    elif inputOption == '3':
        descOption = "text"
    elif inputOption == '4':
        descOption = "person"

    # Create filenames with the timestamp
    filenamej = f"data/{descOption}/{timestamp}.jpg"
    filenamet = f"data/{descOption}/{timestamp}_Text.txt"
    filenamem = f"data/{descOption}/{timestamp}.mp3"
    filenamew = f"data/{descOption}/{timestamp}_Wifi.txt"
    filenamet = f"data/{descOption}/{timestamp}_Time.txt"

    # Capture the screenshot
    screenshot.capture_screenshot()

    # Move and rename the file save in /data/Screenshots path
    screenshot.move_and_rename(filenamej)

    # Convert the OpenCV image to a base64 encoded string
    base64_string = screenshot.convert_image_to_base64(filenamej)

    # Time of printScreen, move, rename and conversion
    printScreenTime = time.perf_counter() - startTime

    if inputOption == '1':
        role = "You are a person that provides professional audio description services. Help me describe the images I show you in Brazilian portuguese."
        text = "Please describe this image. Do not start the phrase with 'A imagem '"

    elif inputOption == '2':
        role = "You are a person that provides professional audio description services for blind people. Help me describe the images I show you in Brazilian portuguese."
        text = "Please describe this image focusing in aiding locomotion for a blind person. I want to know if the way ahead is free for walking. Describe the scene to help me to walk with more confidence, knowing if there is any obstacle in front of me. Be brief, i want a short sentence telling me only the necessary to step foward.'"

    elif inputOption == '3':
        role = "You are a person that provides professional audio description services. Help me describe the images I show you in Brazilian portuguese."
        text = "Please describe this image. Do not start the phrase with 'A imagem '. Read any text you find. focus only on text you can find."

    else:
        role = "You are a person that provides professional audio description services. Help me describe the images I show you in Brazilian portuguese."
        text = "Please describe this image. Do not start the phrase with 'A imagem '. Describe the person in the center of the image. Focus on the facial features. Describe as gently as you can. I'm blind and want to know the person by her face."

    # Capture Wi-Fi details
    wifi_details = parameters.get_wifi_details()
    
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
    
    parameters.save_file_wifi(filenamew, wifi_details)
    
    audio.text_to_speech(text, filenamem, client)

    textToMP3Time = time.perf_counter() - startTime - printScreenTime - responseTime

    audio.play_mp3(filenamem)

    # Time of the audio created
    audioTime = time.perf_counter() - startTime - printScreenTime - responseTime - textToMP3Time

    # Total time of the application
    totalTime = time.perf_counter() - startTime
    
    parameters.save_file_time(filenamet, printScreenTime, responseTime, textToMP3Time, totalTime)