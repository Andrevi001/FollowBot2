from abc import ABC, abstractmethod
from Point import Point
from Identifier.Verdict import Verdict
import numpy as np 

class Identifier(ABC):
    """Abstract class for identification algorithms."""
    
    def __init__(self, portion, threshold):
        """
        Class constructor
        
        Args:
            portion: float in (0, 1], size of the feature extraction region,
                 relative to a reference length (e.g. shoulder width).
                 The region and the keypoint it is centered on are
                 defined by each subclass.
            threshold: float, similarity score aboce which a verification is considered successful.
        """
        
        self._portion = portion
        self._threshold = threshold
        
    @abstractmethod
    def enroll(self, samples: list[(list[Point], list[np.array])]) -> None:
        """
        Used to extract and store the identifying features of the target
        """
        ...

    @abstractmethod
    def verify(self, sample: tuple[list[Point], np.array]) -> Verdict:
        """
        Used, after succesfull enrollement, to compare the given pose against the enrolled target.
        It will return Verdict.MATCH if the comparison is successful, will Verdict.NO_MATCH other wise
        If used before a seccesfull enrolement, it will return Verdict.NOT_ENROLLED.
        If the verification wasn't possible it will return Verdict.NOT_VERIFIABLE.

        Retuns:
            Verdict: indicating the comparison result.
        """
        ...