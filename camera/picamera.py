from picamera2 import Picamera2
from libcamera import Transform

picam2 = Picamera2()
# picam2.configure(picam2.create_still_configuration())
# picam2.start()

camera_config = picam2.create_still_configuration(transform=Transform(hflip=True, vflip=False))

picam2.configure(camera_config)
picam2.start()

def initialize_camera():
    return picam2

def close_camera():
    picam2.stop()
    picam2.close()


if __name__ == "__main__":
    cam = initialize_camera()
    cam.capture_file("test.jpg")