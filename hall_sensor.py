import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)

near_magnetic = True
count = 0

while True:
	## GPIO.input(4) == 1 means near magnetic field, 0 means far from magnetic field
	## far from magnetic field (fridge opened)
	if (not GPIO.input(4)):
		near_magnetic = False
	## near magnetic field (fridge closed)
	if (GPIO.input(4) and near_magnetic == False):
		## take picture and save to database
		count += 1
		print("take picture: ", count)
		near_magnetic = True
	

