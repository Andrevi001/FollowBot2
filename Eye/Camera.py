import picamera2
import cv2
import config
import threading

class Camera():

    def __init__(self):
        self.__frame = []
        self.__new_frame = False
        self._lock = threading.Lock()
        self.picam2 = picamera2.Picamera2()
        self.__running = False

    def begin(self):
        conf = self.picam2.create_preview_configuration(main={"size": (config.width, config.height)})
        self.picam2.configure(conf)
        self.picam2.start()

        self.__thread = threading.Thread(target=self._threaded_capture, daemon=True)
        self.__running = True
        self.__thread.start()

        frame = self.picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.flip(frame, 1)
        self.__frame = frame
        
    def _threaded_capture(self):
        while self.__running:
            frame = self.picam2.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.flip(frame, 1)

            with self._lock:
                self.__new_frame = True
                self.__frame = frame

    def get_frame(self):
        with self._lock:
            if self.__new_frame:
                self.__new_frame = False
                return self.__frame

            return None 

    def close(self):
        self.__running = False

        if self.__thread and self.__thread.is_alive():
            self.__thread.join()

        self.picam2.close()