from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from typing import Self


class Rank(Enum):
    CAD = "cadet"
    OFF = "officer"
    LIE = "lieutenant"
    CAP = "captain"
    COM = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission_rules(self) -> Self:
        val_errs = []

        if not self.mission_id.startswith("M"):
            val_errs.append("Mission ID must start with 'M'")

        if not any(mem.rank in [Rank.COM, Rank.CAP] for mem in self.crew):
            val_errs.append(
                "Mission must have at least one Commander or Captain")

        if self.duration_days > 365:
            exp = sum(1 for mem in self.crew if mem.years_experience >= 5)
            if exp / len(self.crew) < 0.5:
                val_errs.append(
                    "Long missions (> 365 days)"
                    " need 50% experienced crew (5+ years)")

        if not all(member.is_active for member in self.crew):
            val_errs.append("All crew members must be active")

        if val_errs:
            raise ValueError("\n".join(val_errs))

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("========================================\n")
    print("Valid mission created:")

    crew_member_1 = CrewMember(
        member_id="MARS_001",
        name="Sarah Connor",
        rank=Rank.COM.value,
        age=35,
        specialization="Mission Command",
        years_experience=10,
        is_active=True,
    )

    crew_member_2 = CrewMember(
        member_id="MARS_002",
        name="John Smith",
        rank=Rank.LIE.value,
        age=35,
        specialization="Navigation",
        years_experience=10,
        is_active=True,
    )

    crew_member_3 = CrewMember(
        member_id="MARS_003",
        name="Alice Johnson",
        rank=Rank.OFF.value,
        age=35,
        specialization="Engineering",
        years_experience=10,
        is_active=True,
    )

    mission = SpaceMission(
        mission_id="M2026_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date="2026-04-01 00:00:00",
        duration_days=900,
        crew=[crew_member_1, crew_member_2, crew_member_3],
        mission_status="planned",
        budget_millions=2500.0,
    )

    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")

    print("\nCrew members:")
    print(
        f"- {crew_member_1.name} ({crew_member_1.rank.value})"
        f" - {crew_member_1.specialization}"
    )
    print(
        f"- {crew_member_2.name} ({crew_member_2.rank.value})"
        f" - {crew_member_2.specialization}"
    )
    print(
        f"- {crew_member_3.name} ({crew_member_3.rank.value})"
        f" - {crew_member_3.specialization}"
    )

    print("\n=========================================")
    print("Expected validation error:")
    try:
        invalid_crew = CrewMember(
            member_id="MARS_001",
            name="Sarah Connor",
            rank=Rank.OFF.value,
            age=35,
            specialization="Mission Command",
            years_experience=10,
            is_active=True,
        )

        mission = SpaceMission(
            mission_id="N2026_MARS",
            mission_name="Busted Mission",
            destination="Mars",
            launch_date="2026-04-01 00:00:00",
            duration_days=42,
            crew=[invalid_crew],
            mission_status="planned",
            budget_millions=1337,
        )
    except ValidationError as e:
        for err in e.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
