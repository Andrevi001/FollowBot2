import picamera2
import numpy as np
import cv2
from pySerialTransfer import pySerialTransfer as txfer
import traceback

width = 680
height = 480

model = cv2.FaceDetectorYN.create("yunet.onnx", "", (width, height))

picam2 = picamera2.Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (width, height)}
)
picam2.configure(config)
picam2.start()

serial = txfer.SerialTransfer('/dev/serial0', baud=115200)
 
try :
    serial.open()
    print("Seriale attiva")
    send_size = 0

    while True:

        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame, 1)
        _, faces = model.detect(frame)

        if faces is not None:
            for face in faces:
                
                x, y, w, h = face[0:4].astype(int)
                confidence = face[14]
                
                if confidence >= 0.7:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))
                    
                    
                    
                    send_size = serial.tx_obj(80, 0)
                    serial.send(send_size)

        send_size = serial.tx_obj(65, 0)
        serial.send(send_size)
        
        cv2.imshow("camera", frame)

        if cv2.waitKey(1) == 27:
            break

except KeyboardInterrupt:
    print("\nInterruzione da tastiera")

finally:
    picam2.close()
    serial.close()
    cv2.destroyAllWindows()