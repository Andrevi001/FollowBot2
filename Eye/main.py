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
    print("Seriale attiva")

    while True:
        frame = cam.captureFrame()
        
        targets = target_detector.detect(frame)
        if targets is not None:

            targets = target_tracker.processTargets(targets.pose_landmarks)
            for target in targets:
                header, pan, tilt, distance, center = target

                if header == 80:
                    x, y = center
                    cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

                    serial0.write(bytes([header, pan & 0xFF, tilt & 0xFF, distance & 0xFF]))
        else:
            serial0.write(bytes([65, 0, 0, 0]))
        
        
        
        cv2.imshow("camera", frame)

        if cv2.waitKey(1) == 27:
            break
except KeyboardInterrupt:
    print("\nInterruzione da tastiera")

finally:
    cam.close()
    if serial0 is not None and serial0.is_open:
        serial0.close()
    cv2.destroyAllWindows()
