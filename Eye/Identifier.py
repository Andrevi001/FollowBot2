from abc import ABC, abstractmethod
from Point import Point
import numpy as np 

class Identifier(ABC):
    """Abstract interface for identification algorithms."""

    @abstractmethod
    def enroll(self, samples: list[(list[Point], list[np.array])]) -> None:
        """
        Used to extract and store the identifying features of the target
        """
        ...

    @abstractmethod
    def verify(self, sample: tuple[list[Point], np.array]) -> float:
        """
        Used, after succesfull enrollement, to compare the given pose against the enrolled target.
        If used before a seccesfull enrolement, it will return -1.

        Retuns:
            float: Similarity score.
        """
        ...