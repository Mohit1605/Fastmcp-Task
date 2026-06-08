from enum import Enum


class CallStatus(str, Enum):
    OPEN = "OPEN"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class CallOutcome(str, Enum):
    RESOLVED = "RESOLVED"
    VOICEMAIL = "VOICEMAIL"
    NO_ANSWER = "NO_ANSWER"
    CALLBACK_REQUESTED = "CALLBACK_REQUESTED"
    ESCALATED = "ESCALATED"