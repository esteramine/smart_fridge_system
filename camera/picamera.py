from picamera2 import Picamera2

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

def initialize_camera():
    return picam2

def close_camera():
    picam2.stop()
    picam2.close()
