import cv2
import time
import os
import random
import numpy as np 
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

INPUT_IMAGE_PATH = 'captured_image.jpg'
OUTPUT_FILENAME = "Juan.jpg"
MODEL = "gemini-2.5-flash-image"
CAMERA_INDEX = 0
LIVE_WINDOW_NAME = "Live Stream / Screenshot"
STATE_LIVE_STREAM = 0
STATE_PAUSED_IMAGE = 1
SAVED_IMAGE_PATH = "captured_image.jpg"

def main():
    
    client = genai.Client()
    cap = cv2.VideoCapture(CAMERA_INDEX)
    current_state = STATE_LIVE_STREAM
    while True:
        ran = random.randint(1, 7)
        if current_state == STATE_LIVE_STREAM:
            ret, frame = cap.read()
            cv2.imshow(LIVE_WINDOW_NAME, frame)
            live_frame = frame
            key = cv2.waitKey(1) & 0xFF

            if key == ord('s'):
                success = cv2.imwrite(SAVED_IMAGE_PATH, live_frame)

                prompts = {1: '"Make this look like Hieronymus Bosch art."', 2:'"Make this look like dali art."', 3:'"Make this look like Giuseppe Arcimboldo art."',
                           4: '"Make this look like René Magritte art."',5: '"Make this look like Francis Bacon art."',
                           6: '"Make this look like Max Ernst art."', 7: '"Make this look like Jackson Pollock art."'
                           }
                EDIT_PROMPT = prompts[ran]
                
                uploaded_file = client.files.upload(file=INPUT_IMAGE_PATH)
                response = client.models.generate_content(
                    model=MODEL,
                    contents=[EDIT_PROMPT, uploaded_file],
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE", "TEXT"],
                    ),
                )
                image_found = False
                for part in response.parts:

                    if part.inline_data:
                        image_bytes = part.inline_data.data
                        
                        generated_image = Image.open(BytesIO(image_bytes))
                        generated_image.save(OUTPUT_FILENAME)
                        Test = np.array(generated_image)
                        Test = cv2.cvtColor(Test, cv2.COLOR_BGR2RGB)
                        image_found = True
        
                    elif part.text:
                        print(f"Model Commentary: {part.text}")
                

                
                if success:
                    current_state = STATE_PAUSED_IMAGE

            elif key == ord('q'):
                break
        
        elif current_state == STATE_PAUSED_IMAGE:
            if os.path.exists(SAVED_IMAGE_PATH):
                captured_image = cv2.imread(SAVED_IMAGE_PATH)
                if captured_image is not None:

                    cv2.imshow(LIVE_WINDOW_NAME, Test)
                else:
                    current_state = STATE_LIVE_STREAM
            

            key = cv2.waitKey(500) & 0xFF 

            if key == ord('s'):
                current_state = STATE_LIVE_STREAM
            elif key == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    if os.path.exists(SAVED_IMAGE_PATH):
        os.remove(SAVED_IMAGE_PATH)

if __name__ == "__main__":
    main()