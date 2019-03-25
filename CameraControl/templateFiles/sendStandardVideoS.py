from io import BytesIO
from time import sleep
from picamera import PiCamera

myStream = BytesIO()
camera = PiCamera()
camera.capture(myStream, 'h264')
