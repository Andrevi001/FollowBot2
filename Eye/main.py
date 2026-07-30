import cv2
import serial
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from Camera import Camera
from FaceTracker import FaceTracker
from PerformanceTracker import PerformanceTracker

base_options = python.BaseOptions(model_asset_path='Modelli/detector_full_range.tflite')
options = vision.FaceDetectorOptions(
    base_options=base_options,
    min_detection_confidence=0.2
)
detector = vision.FaceDetector.create_from_options(options)

cam = Camera() 
face_tracker = FaceTracker()
performance_tracker = PerformanceTracker("ModelPerformance/MediaPipe_Performance.csv")

try :
    cam.begin()
    serial0 = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    print("Seriale attiva")

    while True:
        tot_latency_start = time.perf_counter()

        frame = cam.captureFrame()
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        inf_latency_start = time.perf_counter()
        result = detector.detect(mp_image)
        inf_latency_finish = time.perf_counter()
        performance_tracker.thisInferenceLatecy((inf_latency_finish-inf_latency_start)*1000)

        send_size = 0
        faces = result.detections
        if faces is not None:

            header, pan, tilt, distance, frame_data = face_tracker.processFaces(faces)
            x, y, w, h = frame_data

            if header == 80:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))        

            serial0.write(bytes([header, pan & 0xFF, tilt & 0xFF, distance & 0xFF]))
        else:
            serial0.write(bytes([65, 0, 0, 0]))
        
        cv2.imshow("camera", frame)

        if cv2.waitKey(1) == 27:
            break
        tot_latency_finish = time.perf_counter()
        performance_tracker.thisLatency((tot_latency_finish-tot_latency_start)*1000)
        performance_tracker.writeToFile()
except KeyboardInterrupt:
    print("\nInterruzione da tastiera")

finally:
    cam.close()
    if serial0 is not None and serial0.is_open:
        serial0.close()
    cv2.destroyAllWindows()
