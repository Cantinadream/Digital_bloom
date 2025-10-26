import cv2
import sys

CAMERA_INDEX = 0 
WINDOW_NAME = "Live Stream / Freeze Frame (Press 's' to toggle, 'q' to quit)"

is_live = True
frozen_frame = None

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print(f"Error: Could not open video stream or file at index {CAMERA_INDEX}")
    sys.exit()

print("Camera is ready. Press 's' to freeze/unfreeze, or 'q' to quit.")

try:
    while True:
        if is_live:
            ret, frame = cap.read()
            if not ret:
                print("Error: Can't receive frame (stream end?). Exiting ...")
                break
            cv2.imshow(WINDOW_NAME, frame)
            
        else:
            if frozen_frame is not None:
                cv2.imshow(WINDOW_NAME, frozen_frame)
            else:
                 is_live = True 
                 continue
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            if is_live:
                frozen_frame = frame.copy() 
                is_live = False
                print("Stream FROZEN. Press 's' to resume live stream.")
            else:

                is_live = True
                frozen_frame = None
                print("Live Stream RESUMED. Press 's' to freeze.")
        elif key == ord('q'):
            print("Quitting application.")
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Cleanup complete.")