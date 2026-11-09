from Identifier.ImageBasedIdentifier import ImageBasedIdentifier
import cv2
import config

class FaceIdentifier(ImageBasedIdentifier):

    def __init__(self, id_size):
        """
        Class contructor

        Args:
            id_size : length of the side of the square identification region.
                      The length is expressed in pixels.
                      The region is centered around the subjects nose.   
        """
        self.__id_size = id_size

    def _preprocessing(self, sample):
        """
        Prepares the given for identification
        
            Args:
                sample: containing pose and corresponing frame
            
            Returns:
                square, grayscale region of self.__id_size dimensions 
        """
        
        pose, frame = sample
        
        nose = pose[0]
        ear_l = pose[7]
        ear_r = pose[8]
            
        padding = 30
        ear_to_ear_distance = self._calculate_distance(ear_l, ear_r)
            
        cropped_frame = self._crop_around(frame, nose, round(padding + ear_to_ear_distance))

        if cropped_frame is None:
            return None

        half = round(padding + ear_to_ear_distance) // 2
        x = int(nose.x * config.width)
        y = int(nose.y * config.height)
        top_left = (x - half, y - half)
        bottom_right = (x + half, y + half)
        if frame is not None:
            img = frame.numpy_view().copy()
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
            cv2.imshow("camera", img)
            cv2.waitKey(1)
            
        gray_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)        
        height, width = gray_frame.shape

        gray_and_resized = gray_frame

        if height >= self.__id_size and width >= self.__id_size:
            gray_and_resized = cv2.resize(gray_frame, (self.__id_size, self.__id_size), interpolation=cv2.INTER_AREA)
        else:
            gray_and_resized = cv2.resize(gray_frame, (self.__id_size, self.__id_size), interpolation=cv2.INTER_LINEAR)
            
        return gray_and_resized 
