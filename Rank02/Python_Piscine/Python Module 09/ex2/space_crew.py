from enum import Enum
from pydantic import BaseModel, Field, model_validator
from datetime import datetime

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

    @model_validator(mode='after')
    def validate_mission_rules(self):
        val_errs = []

        if not self.mission_id.startswith("M"):
            val_errs.append("Mission ID must start with 'M'")

        if not any(member.rank in [Rank.COM, Rank.CAP] for member in self.crew):
            val_errs.append("Mission must have at least one Commander or Captain")

        if self.duration_days > 365:
            experienced_count = sum(1 for member in self.crew if member.years_experience >= 5)
            if experienced_count / len(self.crew) < 0.5:
                val_errs.append("Long missions (> 365 days) need 50% experienced crew (5+ years)")

        if not all(member.is_active for member in self.crew):
            val_errs.append("All crew members must be active")

        if val_errs:
            raise ValueError("\n".join(val_errs))

        return self


def main() -> None:
    pass


if __name__ == "__main__":
    main()
