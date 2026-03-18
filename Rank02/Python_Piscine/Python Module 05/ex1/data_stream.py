#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):

    def __init__(self, stream_id):
        self.stream_id = stream_id
        self.stats = {"total processed": 0}

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any], criteria: Optional[str] = None) -> List[Any]:
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return self.stats


class SensorStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
    def process_batch(self, data_batch: List[Any]) -> str:
        self.stats["total processed"] += len(data_batch)
        temps = []

        for data in data_batch:
            if isinstance(data, dict) and "temp" in data:
                temps.append(float(data["temp"]))
            elif isinstance(data, str) and "temp" in data.lower():
                parts = data.split(":")
                if len(parts) == 2:
                    temps.append(float(parts[1].strip()))

        if len(temps) > 0:
            avg = sum(temps) / len(temps)
        else:
            avg = 0.0

        return f"Sensor analysis: {len(data_batch)} readings processed, avg temp: {avg:.1f}°C"


class TransactionStream(DataStream):

    def __init__(self, stream_id):
        super().__init__(stream_id)
    
    def process_batch(self, data_batch: List[Any]) -> str:
        self.stats["total processed"] += len(data_batch)
        flow = 0

        for item in data_batch:
            if isinstance(item, str) and "buy" in item.lower():
                parts = item.split(":")
                if len(parts) == 2:
                    flow += int(parts[1].strip())
            elif isinstance(item, str) and "sell" in item.lower():
                parts = item.split(":")
                if len(parts) == 2:
                    flow -= int(parts[1].strip())
        
        return f"Transaction analysis: {len(data_batch)} operations, net flow: {flow:+d} units"

class EventStream(DataStream):

    def __init__(self, stream_id):
        super().__init__(stream_id)
    
    def process_batch(self, data_batch: List[Any]) -> str:
        self.stats["total processed"] += len(data_batch)
        errors = 0
        for item in data_batch:
            if isinstance(item, str) and "error" in item.lower():
                errors += 1
        return f"Event analysis: {len(data_batch)} events, {errors} error(s) detected"


def main():
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

    sensor = SensorStream("SENSOR_001")
    data_list = ["temp:22.5", "humidity:65", "pressure:1013"]
    print("\nInitializing Sensor Stream...")
    print(f"Stream ID: {sensor.stream_id}, Type: Enviromental Data")
    print(f"Processing sensor batch: [{', '.join(data_list)}]")
    print(sensor.process_batch(data_list))

    trans = TransactionStream("TRANS_001")
    trans_list = ["buy:100", "sell:150", "buy:75"]
    print("\nInitializing Transaction Stream...")
    print(f"Stream ID: {sensor.stream_id}, Type: Financial Data")
    print(f"Processing transaction batch: [{', '.join(trans_list)}]")
    print(trans.process_batch(trans_list))

    event = EventStream("EVENT_001")
    event_list = ["login", "error", "logout", "error"]
    print("\nInitializing Event Stream...")
    print(f"Stream ID: {event.stream_id}, Type: Financial Data")
    print(f"Processing event batch: [{', '.join(event_list)}]")
    print(event.process_batch(event_list))


if __name__ == "__main__":
    main()
