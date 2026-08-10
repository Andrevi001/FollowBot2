import cv2
import serial
from Camera import Camera
from TargetTracker import TargetTracker
from TargetDetector import TargetDetector

cam = Camera()
target_detector = TargetDetector() 
target_tracker = TargetTracker()

try :
    cam.begin()
    serial0 = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    print("Attivo")
    old_frame = None

    while True:
        new_frame = cam.get_frame()

        if new_frame is not None:
            old_frame = new_frame
            target_detector.detect_async(old_frame)

        detections = target_detector.get_Targets()

        if detections and old_frame is not None:

            targets = target_tracker.processTargets(detections)
            if targets:
                for target in targets:
                    header, pan, tilt, distance, center = target

                    if header == 80:
                        x, y = center
                        cv2.circle(old_frame, (x, y), 3, (0, 255, 0), -1)

                        serial0.write(bytes([header, pan & 0xFF, tilt & 0xFF, int(distance) & 0xFF]))
            else:
                serial0.write(bytes([65, 0, 0, 0]))

        if old_frame is not None:
            cv2.imshow("camera", old_frame)

        if cv2.waitKey(1) == 27:
            break


except KeyboardInterrupt:
    print("\nChiusura in corso")

finally:
    cam.close()
    if serial0 is not None and serial0.is_open:
        serial0.close()
    cv2.destroyAllWindows()