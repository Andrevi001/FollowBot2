from abc import ABC, abstractmethod
from Point import Point

class Identifier(ABC):
    """Abstract interface for identification algorithms."""

    @abstractmethod
    def enroll(self, pose: list[Point]) -> None:
        """
        Used to extract and store the identifying features of the target
        """
        ...

    @abstractmethod
    def verify(self, pose: list[Point]) -> float:
        """
        Used, after succesfull enrollement, to compare the given pose against the enrolled target.

        Retuns:
            float: Similarity score.
        """
        ...