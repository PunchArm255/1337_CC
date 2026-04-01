from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator


class SpaceStation(BaseModel):
    station_id: str
    name: str
    crew_size: int
    power_level: float
    oxygen_level: float



def main() -> None:
    pass


if __name__ == "__main__":
    main()