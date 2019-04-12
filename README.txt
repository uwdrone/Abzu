Code Index:
  Libraries:
    Adafruit BNO055 IMU:
      Directories:
        Adafruit_BNO055.egg-info
        Adafruit_BNO055
        build
        dist
        examples
       Files:
        setup.oy
        ez_setup.py
        LICENSE
    All other libraries are not present on github, but were installed
    on the raspberry pi and used as such. The BNO055 library required
    a special build configuration for our project, and so was included
    in the git repo to ensure consistency. Links to installation guides
    for each library can be found below.
    
  Original Code:
    CameraControl:
      Record.py --Thread that handles recording of video
      Streamer.py --Thread that streams video to webpage
        both utilize picamera library
    MotorControl:
      motor.py --Motor class that wraps around adafruit motor library, used by skid and stick steering to actuate respective motors
      pid.py --PID controller class, used by stickSteering to maintain balance
      skidSteering.py --Thread that handles rear motors. Actuated by right joystick user input
      stickSteering.py --Thread that handles four top motors. Actuation depends on user input, and balance from PID.
    PID: --bit of a misnomer
      imuPolling.py --Thread that polls the imu at a set rate and pushes the input to shared memory
    RemoteControl:
      ControllerReceiver.py --Thread that acts as a server for user input. When user input is received it pushes it shared memory.
      ControllerSender.py --Client applicated for user input. Uses pyUSB library to get input, and sends to server over socket.
    launcherProgram.py --Launches all the above components, houses the shared memory, and synchronization constants.
    Abzu_launch.sh --bash script for running launcherProgram.py on boot
    mv_vids.sh --bash script to scp videos recorded from the pi to user computer
    
  Library Links:
    Adafruit CircuitPython MotorKit
        found at https://github.com/adafruit/Adafruit_CircuitPython_MotorKit
    Picamera
        found at https://picamera.readthedocs.io/en/release-1.13/
    Adafruit Python BNO055 IMU
        found at https://github.com/adafruit/Adafruit_Python_BNO055
    pyUSB
        found at https://github.com/pyusb/pyusb

    For instructions on using the drone visit the ApplicationNotes
