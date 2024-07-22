import re
import subprocess


def get_wifi_details():
    """
    Retrieve detailed WiFi connection statistics using nmcli on Linux.
    
    :parameter(s): None
    
    :return: None
    """
    try:
        # Run the nmcli command to get full details of the active Wi-Fi connection.
        result = subprocess.run(['nmcli', '-t', '-f', 'IN-USE,SSID,BSSID,MODE,CHAN,RATE,SIGNAL,BARS,SECURITY', 'device', 'wifi'], capture_output=True, text=True)
        if result.returncode == 0:
            # Process the output to find the line with the active network (marked with '*').
            for line in result.stdout.splitlines():
                if '*' in line:  # Check if the line contains the active network
                    # Remove unwanted characters
                    cleaned_line = re.sub(r'\\.', '', line)
                    parts = cleaned_line.split(':')
                    details = {
                        'ssid': parts[1],
                        'bssid': parts[2],
                        'mode': parts[3],
                        'channel': parts[4],
                        'rate': parts[5],
                        'signal': parts[6],  # Keep as a temporary string
                        'bars': parts[7],
                        'security': parts[8]
                    }
                    # Try to convert the signal to int, otherwise set as error;
                    try:
                        details['signal'] = int(details['signal'])
                    except ValueError:
                        details['signal'] = "Invalid signal data: " + details['signal']
                    return details
    except Exception as e:
        return {'error': str(e)}

    return {'error': "No active Wi-Fi connection found."}

def save_file_wifi(file_path, wifi_details):
    """
    Define the signal quality and save the wifi details in a .txt file
    
    :parameter(s): 
        filepath: String, the path to the file where the times will be saved.
        wifi_details: Data about some wifi datails collected by nmcli
    
    :return: None
    """
    # Evaluates the signal quality
    if 'signal' in wifi_details and isinstance(wifi_details['signal'], int):
        signal_strength = wifi_details['signal']
        quality_description = "High" if signal_strength > 75 else "Medium" if signal_strength > 50 else "Low"
        wifi_details['quality_description'] = quality_description
    else:
        wifi_details['quality_description'] = "Unavailable"  
    
    # Write the .txt file with the info
    with open(file_path, 'w') as file:
        for key, value in wifi_details.items():
            file.write(f"{key}: {value}\n")

def save_file_time(file_path, printScreenTime, responseTime, textToMP3Time, audioTime, totalTime):
    """
    Saves the execution times of various stages of a process to a file.
    
    :parameter(s):
        filepath: String, the path to the file where the times will be saved.
        printScreenTime: float, the time taken for screen capture, in seconds.
        responseTime: float, the response time from artificial intelligence, in seconds.
        textToMP3Time: float, the time taken to convert text into MP3 audio, in seconds.
        audioTime: float, the playback time of the audio, in seconds.
        totalTime: float, the total time spent in the process, in seconds.

    :return: None
    """
    with open(file_path, 'w') as file:
        file.write(f"PrintScreen time: {printScreenTime}\n" +
                    f"Response from IA time: {responseTime}\n" + 
                    f"Conversion text to MP3 time: {textToMP3Time}\n" +
                    f"Audio time: {audioTime}\nTotal Time: {totalTime}")