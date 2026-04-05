import picamera2
import numpy as np
import cv2

picam2 = picamera2.Picamera2()
picam2.start()

try :
    while True:

        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame, 1)
        cv2.imshow("camera", frame)

        if cv2.waitKey(1) == 27:
            break

except KeyboardInterrupt:
    print("\nInterruzione da tastiera")

finally:
    picam2.close()
    cv2.destroyAllWindows()