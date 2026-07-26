import cv2
import serial
import config
from Camera import Camera
from FaceTracker import FaceTracker

model = cv2.FaceDetectorYN.create("yunet.onnx", "", (config.width, config.height))
cam = Camera() 
face_tracker = FaceTracker()

try :
    cam.begin()
    serial0 = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    print("Seriale attiva")

    while True:

        frame = cam.captureFrame()
        _, faces = model.detect(frame)

        send_size = 0

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

except KeyboardInterrupt:
    print("\nInterruzione da tastiera")

finally:
    cam.close()
    serial0.close()
    cv2.destroyAllWindows()