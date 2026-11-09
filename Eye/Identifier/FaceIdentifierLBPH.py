from Identifier.FaceIdentifier import FaceIdentifier
import cv2
import numpy as np
from Identifier.Verdict import Verdict


class FaceIdentifierLBPH(FaceIdentifier):
    def __init__(self, threshold, id_size):
        """
        Class constructor

            Args:
                threshold: value in (0,1], indicating a similarity score above which a verification is considered successful.
        """

        super().__init__(id_size)
        self.__threshold = threshold
        self.__enrolled = False
        self.__identifier = cv2.face.LBPHFaceRecognizer_create(
            radius=1,
            neighbors=8,
            grid_x=4,
            grid_y=4
        )
        
    def enroll(self, samples):
        
        gray_frames = []
        
        for sample in samples:

            gray_and_resized = self._preprocessing(sample)
            
            if gray_and_resized is not None:
                gray_frames.append(gray_and_resized)
        
        labels = np.zeros(len(gray_frames), dtype=np.int32)
        
        self.__identifier.train(gray_frames, labels)
        
        self.__enrolled = True
    
    def verify(self, sample):
        if not self.__enrolled:
            return Verdict.NOT_ENROLLED
        
        gray_and_resized = self._preprocessing(sample)

        if gray_and_resized is None:
            return Verdict.NOT_VERIFIABLE
        
        label, distance = self.__identifier.predict(gray_and_resized)
        
        max_distance = 4 * self.__identifier.getGridX() * self.__identifier.getGridY()
        similarity = 1 - distance/max_distance
        print(similarity)
        
        if similarity >= self.__threshold:
            return Verdict.MATCH
        else:
            return Verdict.NO_MATCH    