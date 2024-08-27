from picamera2 import Picamera2, Preview
from io import BytesIO
from time import sleep

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())

picam2.start()
sleep(5)
image_stream = BytesIO()
picam2.capture_file(image_stream, format='jpeg')
image_stream.seek(0)
# picam2.capture_file("captured_image.jpg")

with open("saved_image_2.jpg", "wb") as f:
    f.write(image_stream.getbuffer())
picam2.stop()
picam2.close()