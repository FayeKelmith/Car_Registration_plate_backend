from fastapi import FastAPI, UploadFile, File
import cv2 as cv 
import numpy as np
import os
import string
from ultralytics import YOLO
import easyocr

app = FastAPI()

#Model definition
vehicle_model = YOLO('yolov8n.pt')
license_model = YOLO('best.pt')

#Initializing OCR reader
reader = easyocr.Reader(['en'], gpu=True)
#for now there is no GPU, but it's much faster with GPU

#Test parameters
image = cv.imread("videos/car.png")

#LICENSE PLATE FORMATING & RECTIFICATION

# Mapping dictionaries for character conversion
# characters that can easily be confused can be 
# verified by their location - an `O` in a place
# where a number is expected is probably a `0`
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}

# LICENSE PLATE FORMAT VERIFICATION
def license_complies_format(text):
    import string

def license_complies_format(text):
    """Checks if a given license plate complies with Indian standard formats."""
    # Check for standard format (XX YY 1234)
    if len(text) == 7 and all(char.isalnum() for char in text):
        if (text[:2].isupper() and text[2:4].isalnum() and text[4:].isupper()):
            return True

    # Check for format with category letter (XX Y1234)
    if len(text) == 6 and all(char.isalnum() for char in text):
        if (text[:2].isupper() and text[2].isalpha() and text[3:].isdigit()):
            return True

    # Check for BH-series format (XX YY 1234 AA)
    if len(text) == 9 and all(char.isalnum() for char in text):
        if (text.startswith("22 BH") and text[5:8].isdigit() and text[8:].isalpha()):
            return True

    return False
# FORMAT LICENSE PLATE
def format_license(text):
    license_plate_ = ''
    mapping = {0: dict_int_to_char, 1: dict_int_to_char, 4: dict_int_to_char, 5: dict_int_to_char, 6: dict_int_to_char,
               2: dict_char_to_int, 3: dict_char_to_int}
    for j in [0, 1, 2, 3, 4, 5, 6]:
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_

#READING LICENSE PLATE
def read_license_plate(license_plate_crop):
    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        bbox, text, score = detection
        text = text.upper().replace(' ', '')
        print(f"Text: {text}")

         # verify that text is conform to a standard license plate
        if license_complies_format(text):
            # bring text into the default license plate format
            return format_license(text), score

    return None, None


def predict(image):
    #Varibales:
    vehicles = [2,3,5,7]
    results = {}
    
    detections = vehicle_model(image)[0]
    
    for detection in detections.boxes.data.tolist():
        #print(detection)
        if len(detection) == 5:
            x1, y1, x2, y2, score = detection
            class_id = 0
        else:
            x1, y1, x2, y2, score, class_id = detection
        
        if int(class_id) in vehicles and score>0.5:
            vehicle_bounding_boxes = []
            vehicle_bounding_boxes.append([x1,y1,x2,y2,score])
            
            for bbox in vehicle_bounding_boxes:
                roi = image[int(y1):int(y2), int(x1):int(x2)]
                
                #print(bbox)
                
                #license plate detector for region of interest
                
                license_plates = license_model(roi)[0]
                
                
                for license_plate in license_plates.boxes.data.tolist():
                    print(f" plate: {license_plate}")
                    plate_x1,plate_y1,plate_x2,plate_y2,score,_ = license_plate
                    
                    #verify detections
                    #print(license_plate)
                    plate = roi[int(plate_y1):int(plate_y2), int(plate_x1):int(plate_x2)]
                    
                    plate_gray = cv.cvtColor(plate, cv.COLOR_BGR2GRAY)
                    _,plate_threshold = cv.threshold(plate_gray, 64,255,cv.THRESH_BINARY_INV)
                    # testing the output of plate
                    # cv.imwrite('plate.jpg',plate_gray)
                    np_text, np_score = read_license_plate(plate_threshold)
                    if np_text is not None:
                        return {"Plate information":[np_text, np_score]}
                
    return {"Plate information": "no plate detected"}

# results = predict(image)
# print(results)



    """

    #TODO:
    
    #1.Capture function:
    
    def capture_image():
    # Initialize the PiCamera
    with picamera.PiCamera() as camera:
        # Capture an image into a stream
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)

        # Convert the stream to a NumPy array
        nparr = np.frombuffer(stream.getvalue(), dtype=np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return img
    
    #2. 
    """
@app.get("/")
def root():
    return {"Message": "Root"}

@app.post("/predict")
async def predict():
    #Capture an image from camera
    #image = capture_image()
    
    prediction_results = predict(image)
    
    """
    #TODO:
    
    1. Algorithm to process prediction results
    2. Send message using message algorithm
    
    """
    
    return 