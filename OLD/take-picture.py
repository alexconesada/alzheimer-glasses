import cv2
import os
from datetime import datetime

# Open the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Find your Desktop automatically
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

print("Camera opened successfully!")
print("Press 'S' to take a picture.")
print("Press 'Q' to close the camera.")

while True:
    # Capture a frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab frame.")
        break

    # Show the live webcam feed
    cv2.imshow("Laptop Camera", frame)

    # Check keyboard input
    key = cv2.waitKey(1) & 0xFF

    # Take a picture when S is pressed
    if key == ord('s'):
        # Create a unique filename using the current time
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(desktop, f"webcam_{timestamp}.jpg")

        # Save the picture
        if cv2.imwrite(filename, frame):
            print(f"Picture saved to: {filename}")
        else:
            print("Error: Could not save the picture.")

    # Close the camera when Q is pressed
    elif key == ord('q'):
        break

# Release the webcam
cap.release()
cv2.destroyAllWindows()

