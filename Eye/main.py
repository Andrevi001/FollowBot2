import cv2
import serial
from Camera import Camera
from TargetTracker import TargetTracker
from TargetDetector import TargetDetector
from DistanceLogger import DistanceLogger
from TargetSelector import TargetSelector
from ChromaticIdentifier import ChromaticIdentifier
import config

cam = Camera()
target_detector = TargetDetector() 
shoulders_log = DistanceLogger("./Distance/K_Shoulders.txt")
chromatic_id = ChromaticIdentifier(0.4)
target_selector = TargetSelector(chromatic_id, 0.7)
target_tracker = TargetTracker(shoulders_log.K_distance())
log_body_measurements = False
show_frame = False
serial0 = None

def imprint(num_frames):
    """
    Used to capture and store identification data.
    
    Args:
        num_frames: number of frames used to extract the identification data.
    """
    
    samples = []
    cnt = 0
    while cnt < num_frames:
        new_frame = cam.get_frame()
        
        if new_frame is not None:
            target_detector.detect_async(new_frame)
            
            detections, detection_frame,  new_data = target_detector.get_targets()
            
            if detections and new_data:
                samples.append((detections, detection_frame))
                cnt = cnt + 1
    
    target_selector.enroll(samples)
    print("imprinting completed")

def main_loop():
    """main Loop that coordinates the image capture, target detection/processing and movement data transmission."""
    
    old_frame = None
    send_frame = True
    
    while True:
                
        new_frame = cam.get_frame()
        
        if new_frame is not None:
            old_frame = new_frame
            target_detector.detect_async(new_frame)
        
        detections, detection_frame,  new_data = target_detector.get_targets()
            
        if detections and old_frame is not None:
        
            target = target_selector.select(detections, detection_frame)
            trackingInfo, secondaryInfo = target_tracker.processTarget(target)

            if trackingInfo and secondaryInfo:
                for trackingData, secondaryData in zip(trackingInfo, secondaryInfo):
                    pan, tilt, distance = trackingData
                    center, shoulder_r, shoulder_l = secondaryData
        
                    cv2.circle(old_frame, (center[0], center[1]), 3, (0, 255, 0), -1)
        
                    if log_body_measurements and new_data:
                        #Warning: verify that the target is at 100 cm from the rover and that they don't move
                        shoulders_log.add_distance(shoulder_r, shoulder_l)
        
                    if send_frame and not log_body_measurements:
                        serial0.write(bytes([70, pan & 0xFF, tilt & 0xFF, distance & 0xFF]))
                        send_frame = False
                    elif send_frame and log_body_measurements:
                        serial0.write(bytes([76, pan & 0xFF, tilt & 0xFF, distance & 0xFF]))
                        send_frame = False
                    else:
                        send_frame = True
        else:
            serial0.write(bytes([78, 0, 0, 0]))
                
                
        if old_frame is not None and show_frame:
            cv2.imshow("camera", old_frame)
        
        if cv2.waitKey(1) == 27:
            break

try :
    cam.begin()
    serial0 = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    print("Initialized")
    imprint(160)
    main_loop()

except KeyboardInterrupt:
    print("\nTerminating program...")

finally:
    cam.close()
    target_detector.close()
    if serial0 is not None and serial0.is_open:
        serial0.write(bytes([78, 0, 0, 0]))
        serial0.close()
    shoulders_log.writeToFile()
    cv2.destroyAllWindows()