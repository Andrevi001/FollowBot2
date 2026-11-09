from Identifier.FaceIdentifier import FaceIdentifier
import cv2
from Identifier.Verdict import Verdict

class FaceIdentifierMACE(FaceIdentifier):
    def __init__(self, id_size):
        super().__init__(id_size)
        self.__identifier = cv2.face.MACE.create(id_size)
        self.__enrolled = False
        
    def enroll(self, samples):
        gray_frames = []
        
        for sample in samples:

            gray_and_resized = self._preprocessing(sample)
            
            if gray_and_resized is not None:
                gray_frames.append(gray_and_resized)
        
        self.__identifier.train(gray_frames)
        self.__enrolled = True
        
    def verify(self, sample):
        
        if not self.__enrolled:
            return Verdict.NOT_ENROLLED
        
        gray_and_resized = self._preprocessing(sample)

        if gray_and_resized is None:
            return Verdict.NOT_VERIFIABLE
        
        match = self.__identifier.same(gray_and_resized)
        
        if match:
            return Verdict.MATCH
        else:
            return Verdict.NO_MATCH
