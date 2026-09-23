import cv2
import serial
from Camera import Camera
from TargetTracker import TargetTracker
from TargetDetector import TargetDetector
from DistanceLogger import DistanceLogger

cam = Camera()
target_detector = TargetDetector() 
shoulders_log = DistanceLogger("K_Shoulders.txt")
shoulder_elbow_log = DistanceLogger("K_Shoulder_Elbow.txt")
target_tracker = TargetTracker(shoulders_log.K_distance(), shoulder_elbow_log.K_distance())
log_body_measurements = False
serial0 = None


"""main Loop that coordinates the image capture, target detection/processing and movement data transmission."""
try :
    cam.begin()
    serial0 = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    old_frame = None
    send_frame = True
    print("Intialized")

    while True:
        new_frame = cam.get_frame()

        if new_frame is not None:
            old_frame = new_frame
            target_detector.detect_async(new_frame)

        detections = target_detector.get_targets()

        if detections and old_frame is not None:

            trackingInfo, secondaryInfo = target_tracker.processTargets(detections)

            if trackingInfo and secondaryInfo:
                for trackingData, secondaryData in zip(trackingInfo, secondaryInfo):
                    header, pan, tilt, distance = trackingData
                    center, shoulder_l, shoulder_r, elbow_r = secondaryData 

                    if header == 80:
                        x, y = center
                        cv2.circle(old_frame, (x, y), 3, (0, 255, 0), -1)

                        if log_body_measurements:
                            shoulders_log.add_distance(shoulder_l, shoulder_r)
                            shoulder_elbow_log.add_distance(shoulder_r, elbow_r)

                        if send_frame:
                            serial0.write(bytes([header & 0xFF, pan & 0xFF, tilt & 0xFF, int(distance) & 0xFF]))
                            send_frame = False
                        else:
                            send_frame = True
            else:
                serial0.write(bytes([65, 0, 0, 0]))

        
        if old_frame is not None:
            cv2.imshow("camera", old_frame)

        if cv2.waitKey(1) == 27:
            break


except KeyboardInterrupt:
    print("\nTerminating program...")

finally:
    cam.close()
    target_detector.close()
    if serial0 is not None and serial0.is_open:
        serial0.close()
    shoulders_log.writeToFile()
    shoulder_elbow_log.writeToFile()
    cv2.destroyAllWindows()