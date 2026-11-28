import cv2
import sys
import time

def enable_camera(pi=False, show_preview=False):
    camera_device = None

    try:
        if pi:
            from picamera2 import Picamera2, Preview

            camera_device = Picamera2()

            config = camera_device.create_video_configuration(
                main={
                    "size": (640, 480),
                    "format": "RGB888"
                },
                controls={"FrameRate": 10},
                buffer_count=3
            )

            camera_device.configure(config)
            if show_preview:
                camera_device.start_preview(
                    Preview.DRM,
                    x=0,
                    y=0,
                    width=640,
                    height=480
                )
            camera_device.start()

            time.sleep(2)

        else:
            camera_device = cv2.VideoCapture(0)

            if not camera_device.isOpened():
                raise RuntimeError("Could not open webcam.")

        print("Camera opened successfully!")
        return camera_device

    except Exception as e:
        print(f"Error enabling camera: {e}", file=sys.stderr)

        if camera_device is not None:
            disable_camera(camera_device, pi)

        return None


def read_camera(camera_device, pi=False):
    try:
        if pi:
            return True, camera_device.capture_array("main")
        else:
            return camera_device.read()

    except Exception as e:
        print(f"Error reading camera: {e}", file=sys.stderr)
        return False, None


def disable_camera(camera_device, pi=False):
    try:
        if camera_device is not None:
            if pi:
                try:
                    camera_device.stop()
                    camera_device.stop_preview()
                finally:
                    camera_device.close()
            else:
                camera_device.release()

    except Exception as e:
        print(f"Error closing camera: {e}", file=sys.stderr)

    finally:
        try:
            cv2.destroyAllWindows()
        except cv2.error:
            pass
