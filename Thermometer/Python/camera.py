import time
import picamera

with picamera.PiCamera() as camera:
	camera.resolution = (1024, 768)
    filename = str(time.localtime) + '.jpg'
    camera.capture(time.localtime)