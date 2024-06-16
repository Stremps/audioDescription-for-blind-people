# Audio Description Application

This application captures the screen, generates an audio description using the ChatGPT4o API, and saves the image along with the generated audio description text and MP3 file.

## Instructions

1. **Connect to WiFi**
   - Ensure both your PC and Meta Quest 3 are connected to the same WiFi network.

2. **Install Dependencies**
   - Open a terminal or command prompt on your PC.
   - Navigate to the directory where this project is located.
   - Install the necessary dependencies by running the following command:
     ```sh
     pip install -r requirements.txt
     ```

3. **Start the Application**
   - Start the Python application by running the following command:
     ```sh
     python audiodescriptionPerson.py
     ```

4. **Browser Setup**
   - Let the browser screen open in full screen mode. This allows the Python application to capture the screen effectively and send it to the ChatGPT4o API for processing.

5. **Output Data**
   - The input image, along with the generated audio description text and MP3 file, will be saved in the `data` folder within the project directory.

## Notes
- Ensure you have all the necessary dependencies installed to run the Python application.
- Make sure your firewall or network settings do not block communication between your PC and Meta Quest 3.
