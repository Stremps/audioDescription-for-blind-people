import subprocess


def boot_start():
    """
    Play an MP3 file in Meta Quest 3 when the code start
    
    :parameter(s): None
    
    :return: None
    """
    
    #Check the creation of the AudioDesc folder in the Meta Quest 3 directory.
    folder_command = "adb shell '[ -d \"/sdcard/AudioDesc\" ] || mkdir \"/sdcard/AudioDesc\"'"
    
    #Execute the folder command
    subprocess.run(folder_command, shell=True, text=True, check=True)
    
    #Move the boot audio to Meta Quest 3, overwriting the previous audio.mp3
    move_command = f"adb push sounds/Boot_Sound.mp3 /sdcard/AudioDesc/audio.mp3"
    
    # Move the designated file
    subprocess.run(move_command, shell=True, text=True, check=True)
    
    # Play the audio
    play_command = "adb shell am start -a android.intent.action.VIEW -d file:///sdcard/AudioDesc/audio.mp3 -t audio/mp3"
    
    subprocess.run(play_command, shell=True, text=True, check=True)

def play_mp3(file_path):
    """
    Play an MP3 file in Meta Quest 3

    :parameter(s):
        file_path: Path to the MP3 file
    
    :return: None
    """
    
    #Move the created audio to Meta Quest 3, overwriting the previous audio.mp3
    move_command = f"adb push {file_path} /sdcard/AudioDesc/audio.mp3"
    
    # Move the designated file
    subprocess.run(move_command, shell=True, text=True, check=True)
    
    # Play the audio
    play_command = "adb shell am start -a android.intent.action.VIEW -d file:///sdcard/AudioDesc/audio.mp3 -t audio/mp3"
    
    subprocess.run(play_command, shell=True, text=True, check=True)
    
def text_to_speech(text, file_path, client):
    """
    Play an MP3 file in Meta Quest 3

    :parameters:
        text: String, text 
        file_path: String, path to the MP3 file
    
    :return: none
    """
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )

    response.stream_to_file(file_path)