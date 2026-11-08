from Identifier.ImageBasedIdentifier import ImageBasedIdentifier
from Point import Point
import numpy as np
from Identifier.Verdict import Verdict


class ChromaticIdentifier(ImageBasedIdentifier):
    def __init__(self, threshold, portion, adaptation_rate : float):
        """
        Class constructor

            Args:
                threshold: same as Identifier.
                portion: float in (0, 1], size of the feature extraction region,
                         relative to a reference length (e.g. shoulder width).
                         The region and the keypoint it is centered on are
                         defined by each subclass.
                adaptation_rate : rate at which the enrolled value adapts to a match.
        """

        super().__init__(threshold)
        self.__portion = portion
        self.__id = None
        self.__adaptation_rate = adaptation_rate
    
    def enroll(self, samples):
        mean_colors = []
        for pose, frame in samples:
            mean_color = self._calculate_mean_color(pose, frame)
            
            if mean_color is not None:
                mean_colors.append(mean_color)
        
        self.__id = np.mean(mean_colors, axis=0)

    def verify(self, sample):
        """
        Same as Identifier, but on Verdict.MATCH the onrolled value is adapted 
        to the matched value according to self.__adaptation_rate
        """
        
        if self.__id is None:
            return Verdict.NOT_ENROLLED
        
        pose, frame = sample
        subject_mean_color = self._calculate_mean_color(pose, frame)
        
        if subject_mean_color is None:
            return Verdict.NOT_VERIFIABLE
        
        for identity, subject in zip(self.__id, subject_mean_color):
            similarity = 1 - abs(identity - subject) / 255
            
            if similarity < self._threshold:
                return Verdict.NO_MATCH

        self._adapt(subject_mean_color)

        return Verdict.MATCH

    def _adapt(self, observerd_value) :
        self.__id = self.__id * (1 - self.__adaptation_rate) + observerd_value * self.__adaptation_rate


    def _calculate_mean_color(self, pose, frame):
        """
        Calculates the mean color of the pose in the frame.
        The average is calculated over the torso region of the pose. 
        The size of the region depends on the subjects distance.
        
        Args:
            pose: List of Point that contains the pose keypoints.
            frame: numpy.array, frame that is relative to the given keypoints.
        Returns:
            numpy.array that contains the average color in RGB format, [R, G, B]
        """

        shoulder_l = pose[11]
        shoulder_r = pose[12]
            
        shoulder_center = Point((shoulder_l.x + shoulder_r.x)/2, (shoulder_l.y + shoulder_r.y)/2 + 0.05, (shoulder_l.visibility + shoulder_r.visibility)/2)

        distance = self._calculate_distance(shoulder_l, shoulder_r)
        pixels = max(30, int(round(distance*self.__portion)))

        cropped_frame = self._crop_around(frame, shoulder_center, pixels)
        
        if cropped_frame is None:
            return None
        
        return  np.mean(cropped_frame, axis=(0, 1))