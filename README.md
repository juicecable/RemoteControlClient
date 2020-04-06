# RemoteControlClient
Client for remotely controlling Jetson Nano and Myrio

### Requirements:
- Windows machinene connected to the internet with non-changing IP
- Python 3.6 or higher
- Pygame installed in Python
- A Joystick or Gamecontroller with a Joystick
- Opencv installed in Python
- Pillow installed in Python
- Numpy installed in Python
- PyTurboJPEG installed in Python (https://pypi.org/project/PyTurboJPEG/)
- LibJPEG-Turbo installed in > C:\libjpeg-turbo-gcc
    - Can be found at (https://github.com/libjpeg-turbo/libjpeg-turbo/releases)
    
    
### First Time Usage:
1. Make sure you are complying with the Liscence before you modify the code
2. Get the server IP Address
3. Get the server port
4. Get the server video port
5. In client.py, Set host to the server IP Address
6. In client.py, Set port to the server port (which by default is 8081)
7. In videoview.py, Set port to the server video port (which by default is 8082)
8. Leave everything else as default
9. Open your remote controller machiene's firewall TCP ports to the server port, and the server video port (which by default is port 8081 and 8082)
10. Plug your game controller / joystick, into your machiene
11. Make sure you are on an IP Address that is accessable by the server (meaning the server can connect to you on that IP)
    1. VPN works, so does being on the same LAN
    2. If you are not on the same LAN (or VPN), then you must use port forwarding
12. Make sure the server is running, and you have access to it
13. Run client.py using Python3
14. The client should display a 4 digit number if it connected correctly
15. Copy that 4 digit number to the server's terminal, and hit enter on the server's terminal
16. You should now see that it is sucessfully running, if you entered the number correctly
    1. If you didn't enter the number correctly, the server should state that the number was wrong
        1. If you entered it wrong, go to back to step 13
17. Everything should be running, please review controls and then mitigations

### Usage:
1. Make sure you are complying with the Liscence before you modify the code
2. Get the server IP Address
3. In client.py, Set host to the server IP Address
4. Plug your game controller / joystick, into your machiene (if it isn't already)
5. Make sure you are on an IP Address that is accessable by the server (meaning the server can connect to you on that IP)
    1. VPN works, so does being on the same LAN
    2. If you are not on the same LAN (or VPN), then you must use port forwarding
6. Make sure the server is running, and you have access to it
7. Run client.py using Python3
8. The client should display a 4 digit number if it connected correctly
9. Copy that 4 digit number to the server's terminal, and hit enter on the server's terminal
10. You should now see that it is sucessfully running, if you entered the number correctly
    1. If you didn't enter the number correctly, the server should state that the number was wrong
        1. If you entered it wrong, go to back to step 7
11. Everything should be running, please review controls and then mitigations


### Controls:
- On the left joystick
    - Up is Forwards
    - Down is Backwards
    - Right is Clockwise Rotation
    - Left is Counter-Clockwise Rotation
- On the Keyboard (with the popup video window selected)
    - The q key disconnects the and closes the client
- On the Keyboard (with the client terminal selected)
    - The ctrl+c key combo restarts the video

### Mitigations:
- In the case that the video window that pops up, with windows stating the video window has stopped responding
    - Please click on the client.py window, then press ctrl-c
- If the robot isn't moving when you move the left joystick, given you have sucessfully got the client connected and running
    - Please press the mode switch on your Game Controller / Joystick, then see if the problem persists
