import cv2
import sys
import os
import datetime

CAMERA_INDEX = 0 
WINDOW_NAME = "Live Stream (Press 's' to capture, 'q' to quit)"
DESKTOP_PATH = "/home/Cantinadream/Desktop"

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print(f"Error: Could not open video stream at index {CAMERA_INDEX}")
    sys.exit()

def save_frame(frame):
    """Generates a timestamped filename and saves the image to the Desktop."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"capture_{timestamp}.jpg"
    
    file_path = os.path.join(DESKTOP_PATH, filename)
    
    success = cv2.imwrite(file_path, frame)
    
    if success:
        print(f"\n Image SAVED successfully to: {file_path}")
    else:
        print("\n Failed to save image.")

print("Press 's' to capture a frame, or 'q' to quit.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error")
            break
        
        cv2.imshow(WINDOW_NAME, frame)
            
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            save_frame(frame)
        elif key == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Cleanup complete.")