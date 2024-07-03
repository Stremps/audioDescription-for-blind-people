## Instructions to setup and play

1. **Connection between dispositives**
   - Ensure your computer and Meta Quest 3 are Connected to each other via cable
   

2. **Install Dependencies**
   - Open a terminal or command prompt on your PC.
   - Navigate to the directory where this project is located.
   - Install the necessary dependencies by running the following command:
     ```sh
     pip install -r requirements/requirements.txt
     ```

3. **Verify Connection with ADB**
   - You should do this step after install all the dependencies.
   - Open a terminal or command prompt on your PC.
   - Verify the connection with the device by running the following command:
     ```sh
     adb devices
     ```
   - In your terminal or command prompt, at least one device should appear in the list of devices attached

4. **Install a media player in Meta Quest 3**
   - You should after connect and allow your computer to debbug in Meta Quest 3.
   - Open a terminal or command prompt on your PC
   - Install the VLC player (recommended) by the following adb command:
      ```sh
     adb install requirements/vlc-3-5-4.apk
     ```
   - Make sure that the media player is installed

4. **Start the Application**
   - Start the Python application by running the following command:
     ```sh
     python audiodescription.py
     ```

5. **Output Data**
   - The input image, along with the generated audio description text and MP3 file, will be saved in the `data` folder within the project directory. Each algorithm have your respectively folder.

## Notes
- Ensure you have all the necessary dependencies installed to run the Python application.
- Make sure that you have allowed Meta Quest 3 USB debugging with your computer
- Make sure that your media player is allowed to open files
- Make sure that your GPT4o API Key are in a file called "Api_key.txt"

## Important Disclaimer
- All your's screen capture in Meta Quest 3 data *WILL BE ERASED*
- The application make a folder called AudioDesc, in this folder the audio will be placed
