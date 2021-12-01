
# Import package


import RPi.GPIO as GPIO
import time
import faceRecognition as fR


# raspberry pi sensor

def sensor():
    time.sleep(1)
    f = open("data.txt","w")

    # GPIO pin setup
    GPIO.setmode(GPIO.BCM)
    pirPin=7
#    light=18
    sound=9

    GPIO.setup(pirPin,GPIO.IN)
#    GPIO.setup(light,GPIO.OUT)
    GPIO.setup(sound,GPIO.IN)

    inputPirpin = GPIO.input(pirPin)
    inputSound = GPIO.input(sound)

    if (inputPirpin == GPIO.LOW) and (inputSound == GPIO.LOW):
        modelTestData = fR.faceRecognition()
        if modelTestData != 0:
            f.write("2 1 1 " + modelTestData)
            f.close()
#            GPIO.output(light, GPIO.HIGH)
            return 1
        elif modelTestData == 0:
            f.write("1 1 1 Null")
            f.close()
            return 1
    elif (inputPirpin == GPIO.HIGH) and (inputSound == GPIO.LOW):
        f.write("0 1 0 Null")
        f.close()
        return 0
    elif (inputPirpin == GPIO.LOW) and (inputSound == GPIO.HIGH):
        f.write("0 0 1 Null")
        f.close()
        return 0
    else:
        f.write("0 0 0 Null")
        f.close()
        return 0


# main function


if __name__ == "__main__":
    sensor()