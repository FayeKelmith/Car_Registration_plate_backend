from model import prediction
from db import get_number
from message import send_message
#from capture import capture_image
import time

#to test without raspberry pi
import cv2 as cv

sleep_time = 60
#NOTE: Capture image and send message every 4 minutes

while True:
    #Capture image
    image = cv.imread("videos/car.png")
    #image = capture_image()
    
    #Detect vehicle
    vehicle = prediction(image)  
    #Check if vehicle is in database
    if vehicle:
        #Get the number from database
        target = get_number(vehicle['information'][0])
        
        #Send message
        try:
            print("target",target)
            send_message(target)
            print("Message sent")
        except Exception as e:
            print("Number not found")
        #Wait for 4 minutes
        time.sleep(sleep_time)
    else:
        #Wait for 4 minutes
        print("No vehicle detected")
        time.sleep(sleep_time)
    