from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")

    ISS = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2026-04-01 00:00:00",
        is_operational=True
        )

    print(f"ID: {ISS.station_id}")
    print(f"Name: {ISS.name}")
    print(f"Crew: {ISS.crew_size} people")
    print(f"Power: {ISS.power_level}%")
    print(f"Oxygen: {ISS.oxygen_level}%")
    print(f"Status: {'Operational' if ISS.is_operational else 'Maintenance'}")

    print("========================================")
    print("Expected validation error:")

    try:
        ISS = SpaceStation(
            station_id="ISS002",
            name="International Space Station dial Jumia",
            crew_size=42,
            power_level=0.0,
            oxygen_level=0.0,
            last_maintenance="2026-04-01 00:00:00",
            is_operational=False
        )
    except ValidationError as e:
        for err in e.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
