from enum import Enum

class Verdict(Enum):
    """
    Enum indicating the possible outcomes of Identifier.verify()
    """
    
    MATCH = "match"
    NO_MATCH = "no_match"
    NOT_ENROLLED = "not_enrolled"
    NOT_VERIFIABLE = "not_verifiable"