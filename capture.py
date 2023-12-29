#NOTE: Control panel
#TODO:
import picamera
import io
import cv2 as cv
import numpy as np
"""PLAN:
    Run raspberrypi here with all control
    """

def capture_image():
# Initialize the PiCamera
    with picamera.PiCamera() as camera:
        # Capture an image into a stream
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg')
        stream.seek(0)

        # Convert the stream to a NumPy array
        nparr = np.frombuffer(stream.getvalue(), dtype=np.uint8)
        img = cv.imdecode(nparr, cv.IMREAD_COLOR)

    return img