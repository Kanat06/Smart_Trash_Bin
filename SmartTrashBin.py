import cv2
from cvzone.ClassificationModule import Classifier
import RPi.GPIO as GPIO
import time

# Set the GPIO mode and pin numbers
GPIO.setmode(GPIO.BOARD)
IN1 = 11  # GPIO pin connected to IN1 of ULN2003
IN2 = 13  # GPIO pin connected to IN2 of ULN2003
IN3 = 15  # GPIO pin connected to IN3 of ULN2003
IN4 = 16  # GPIO pin connected to IN4 of ULN2003

IN01 = 18  # GPIO pin connected to IN1 of ULN2003
IN02 = 22  # GPIO pin connected to IN2 of ULN2003
IN03 = 24  # GPIO pin connected to IN3 of ULN2003
IN04 = 26 

# Set up GPIO pins as outputs
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

GPIO.setup(IN01, GPIO.OUT)
GPIO.setup(IN02, GPIO.OUT)
GPIO.setup(IN03, GPIO.OUT)
GPIO.setup(IN04, GPIO.OUT)

# Define the motor control sequences
step_sequence = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

step_sequence2 = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

# Function to set motor step
def set_step(step):
    GPIO.output(IN1, step[0])
    GPIO.output(IN2, step[1])
    GPIO.output(IN3, step[2])
    GPIO.output(IN4, step[3]

# Function to set motor2 step
def set_step2(step):
    GPIO.output(IN01, step[0])
    GPIO.output(IN02, step[1])
    GPIO.output(IN03, step[2])
    GPIO.output(IN04, step[3]

# Function to rotate motor
def rotate_motor(steps, delay):
    if steps > 0:
        for _ in range(steps):
            for step in step_sequence:
                set_step(step)
                time.sleep(delay)
    elif steps < 0:
        for _ in range(abs(steps)):
            for step in reversed(step_sequence):
                set_step(step)
                time.sleep(delay)

# Function to rotate motor2
def rotate_motor0(steps, delay):
    if steps > 0:
        for _ in range(steps):
            for step in step_sequence2:
                set_step2(step)
                time.sleep(delay)
    elif steps < 0:
        for _ in range(abs(steps)):
            for step in reversed(step_sequence2):
                set_step2(step)
                time.sleep(delay)

cap = cv2.VideoCapture(0)
cr = Classifier('keras_model.h5', 'labels.txt')

try:
    # Initial 360-degree rotation to the right
    rotate_motor(steps=500, delay=0.005)
    rotate_motor(steps=-142, delay=0.005)

    while True:
        # Capture video frame from the camera
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        pd = cr.getPrediction(frame)  # Get object classification prediction

        cv2.imshow("Frame", frame)  # Display the video frame

        cv2.waitKey(1)  # Refresh the OpenCV window

        if pd[1] != 5:  # If a different object is recognized
            if pd[1] == 0:  # Classify object as 0
                # Perform motor movements based on the classification
                rotate_motor(-130, 0.005)
                rotate_motor0(69, 0.005)
                rotate_motor0(-69, 0.005)
                rotate_motor(130, 0.005)
                time.sleep(4)  # Sleep for 4 seconds

                # Capture and display stored frame
                ret, stored_frame = cap.read()
                stored_frame = cv2.resize(stored_frame, (640, 480))
                cv2.imshow("Frame", stored_frame)
                cv2.waitKey(1)

                for _ in range(3):
                    cap.read()  # Read frames to clear buffer

            # Other classification cases (1, 2, 3, 4) can be handled similarly

        if cv2.waitKey(1) & 0xFF == 27:  # If the 'Esc' key is pressed, exit the loop
            break

except KeyboardInterrupt:
    pass

# Clean up GPIO settings when the program exits
GPIO.cleanup()
cap.release()
cv2.destroyAllWindows()
