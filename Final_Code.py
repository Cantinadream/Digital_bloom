import cv2
import sys
import os
import time
import random
import numpy as np 
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO


CAMERA_INDEX = 0
OPENCV_CAMERA_BACKEND = cv2.CAP_V4L2
WINDOW_NAME = "Live Stream (Press 's' to capture, 'q' to quit)"
MODEL = "gemini-2.5-flash-image"


DESKTOP_PATH = "/home/Cantinadream/Desktop/"
DESKTOP_DONE = "/home/Cantinadream/Desktop/capture_test.jpg"
live = True
frozen = None
flag = True

if not os.path.isdir(DESKTOP_PATH):
    print(f"Error: Desktop directory not found at {DESKTOP_PATH}")
    sys.exit()


cap = cv2.VideoCapture(CAMERA_INDEX,OPENCV_CAMERA_BACKEND)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,900)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)


def save_frame(frame):
    filename = f"capture_test.jpg"
    file_path = os.path.join(DESKTOP_PATH, filename)
    success = cv2.imwrite(file_path, frame)
    

try:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,900)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
    client = genai.Client()
    while True:
        ran = random.randint(1, 7)
        if live:
            flag = True
            ret, frame = cap.read()
            if not ret:
                break
        

            cv2.imshow(WINDOW_NAME, frame)

        else:
            if frozen is not None:
                cv2.imshow(WINDOW_NAME,frozen)
                if flag != True :
                    uploaded_file = client.files.upload(file=DESKTOP_DONE)
                    prompts = {1: '"Make this look like Hieronymus Bosch art."', 2:'"Make this look like dali art."', 3:'"Make this look like Giuseppe Arcimboldo art."',
                               4: '"Make this look like René Magritte art."',5: '"Make this look like Francis Bacon art."',
                               6: '"Make this look like Max Ernst art."', 7: '"Make this look like Jackson Pollock art."'
                               }
                    EDIT_PROMPT = prompts[ran]
                    try:
                        response = client.models.generate_content(
                            model=MODEL,
                            contents=[EDIT_PROMPT, uploaded_file],config=types.GenerateContentConfig(response_modalities=["IMAGE","TEXT"],
                                                                                                 ),
                            )
                    except Exception as e:
                        client.files.delete(name=uploaded_file.name)
                        exit()
                    for part in response.parts:
                        if part.inline_data:
                            image_bytes=part.inline_data.data
                            generate_image = Image.open(BytesIO(image_bytes))
                            generate_image.save("/home/Cantinadream/Desktop/test.jpg")
                            print(f"Model Comments: {part.text}")
                    
                    client.files.delete(name=uploaded_file.name)
                    flag = True
                AI = cv2.imread("/home/Cantinadream/Desktop/test.jpg")
                cv2.imshow(WINDOW_NAME,AI)
            else:
                live = True
                continue
                
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            if live:
                frozen = frame.copy()
                flag = False 
                save_frame(frame)
                live = False
            else:
                frozen = None
                is_live = True
        elif key == ord('q'):
            print("Quitting application.")
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Cleanup complete.")