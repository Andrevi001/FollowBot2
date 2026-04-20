import picamera2
import numpy as np
import cv2
import serial
import traceback

width = 680
height = 480

model = cv2.FaceDetectorYN.create("yunet.onnx", "", (width, height))
 
try :
    picam2 = picamera2.Picamera2()
    config = picam2.create_preview_configuration(
        main={"size": (width, height)}
    )
    picam2.configure(config)
    picam2.start()

    serial0 = serial.Serial('/dev/serial0', baudrate=115200)
    print("Seriale attiva")

    while True:

        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame, 1)
        _, faces = model.detect(frame)

        send_size = 0

        if faces is not None:
            for face in faces:
                
                x, y, w, h = face[0:4].astype(int)
                confidence = face[14]
                
                if confidence >= 0.7:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))
                    
                    offset_x = (x + w/2) - (width/2)
                    offset_y = (y + h/2) - (height/2)
                    
                    pan = 0
                    tilt = 0
                    if abs(offset_x) > 5:
                        pan = offset_x * (40/width) *0.4
                    if abs(offset_y) > 5: 
                        tilt = offset_y * (30/height)*0.4
                    
                    serial0.write(bytes([80, int(pan) & 0xFF, int(tilt) & 0xFF]))
                else:
                    serial0.write(bytes([65, 0, 0]))
        else:
            serial0.write(bytes([65, 0, 0]))
        
        cv2.imshow("camera", frame)

        if cv2.waitKey(1) == 27:
            break

except KeyboardInterrupt:
    print("\nInterruzione da tastiera")

finally:
    picam2.close()
    cv2.destroyAllWindows()