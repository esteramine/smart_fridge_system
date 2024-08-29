import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

has_light = False
count = 0

while True:
	## GPIO.input(4) == 1 means no light, 0 means has light
	## has light (fridge opened)
	if (not GPIO.input(4)):
		has_light = True
	## no light (fridge closed)
	if (GPIO.input(4) and has_light == True):
		## take picture and save to database
		count += 1
		print("take picture: ", count)
		has_light = False
	

