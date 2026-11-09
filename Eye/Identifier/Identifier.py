from abc import ABC, abstractmethod
from Point import Point
from Identifier.Verdict import Verdict
import mediapipe as mp

class Identifier(ABC):
    """Abstract class for identification algorithms."""
        
    @abstractmethod
    def enroll(self, samples: list[(list[Point], list[mp.Image])]) -> None:
        """
        Used to extract and store the identifying features of the target
        """
        ...

    @abstractmethod
    def verify(self, sample: tuple[list[Point], mp.Image]) -> Verdict:
        """
        Used, after succesfull enrollement, to compare the given pose against the enrolled target.
        It will return Verdict.MATCH if the comparison is successful, will Verdict.NO_MATCH other wise
        If used before a seccesfull enrolement, it will return Verdict.NOT_ENROLLED.
        If the verification wasn't possible it will return Verdict.NOT_VERIFIABLE.

        Retuns:
            Verdict: indicating the comparison result.
        """
        ...