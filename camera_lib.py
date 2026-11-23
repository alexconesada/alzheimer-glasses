import cv2
import sys

# --------------------------------
# Open webcam
# --------------------------------
def enable_camera():
    try:
        camera_device = cv2.VideoCapture(0)

        if not camera_device.isOpened():
            print("Error: Could not open webcam.", file=sys.stderr)
            return None

        print("Camera opened successfully!")
        return camera_device

    except Exception as e:
        print(f"Error enablikng camera: {e}", file=sys.stderr)
        return None


# --------------------------------
# Clean up camera environment
# --------------------------------
def disable_camera(camera_device):
    try:
        camera_device.release()
        cv2.destroyAllWindows()
    except:
        pass
