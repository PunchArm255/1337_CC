from enum import Enum
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class ContactType(Enum):
    RAD="radio"
    VIS="visual"
    PHY="physical"
    TEL="telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(max_length=500)
    is_verified: bool = Field(default=True)


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")

    AC = AlienContact(
        contact_id="AC_2026_001",
        timestamp="2026-04-01 00:00:00",
        location="Area 51, Nevada",
        contact_type=ContactType.RAD.value,
        signal_strength= 8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=True
    )

    print(f"ID: {AC.contact_id}")
    print(f"Type: {AC.contact_type.value}")
    print(f"Location: {AC.location}")
    print(f"Signal: {AC.signal_strength}/10")
    print(f"Duration: {AC.duration_minutes} minutes")
    print(f"Witnesses: {AC.witness_count}")
    print(f"Message: {AC.message_received}")

    print("======================================")
    print("Expected validation error:")

    try:
        pass
    except ValidationError as e:
        for err in e.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()