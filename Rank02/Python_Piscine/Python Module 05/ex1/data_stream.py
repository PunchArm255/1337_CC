#!/usr/bin/env python3


from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):

    def __init__(self, stream_id: str):
        self.stream_id = stream_id

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any]
                    , criteria: Optional[str] = None) -> List[Any]:
        if criteria is None:
            return data_batch
        filtered = [item for item in data_batch if item == criteria]
        return filtered

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"total processed": 0}


class SensorStream(DataStream):

    def __init__(self, stream_id):
        super().__init__(stream_id)
        self.stream_id = stream_id
        self.stats = 0

    def process_batch(self, data_batch: List[Any]) -> str:
        if isinstance(data_batch, list) is False:
            raise ValueError("Invalid data format.")

        temps = []
        for item in data_batch:
            if "temp" in item.lower():
                temps.append(float(item.split(":")[1]))
        
        avg = sum(temps) / len(temps)
        self.stats = len(data_batch)
        return f"Sensor analysis: {self.stats} readings processed, avg temp: {avg}°C"

    def filter_data(self, data_batch: List[Any]
                    , criteria: Optional[str] = None) -> List[Any]:
        if criteria == "critical":
            fltrd = [item for item in data_batch if float(item.split(":")[1]) > 40]
            return fltrd
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"readings processed": self.stats}


class TransactionStream(DataStream):

    def __init__(self, stream_id):
        super().__init__(stream_id)
        self.stream_id = stream_id

    def process_batch(self, data_batch: List[Any]) -> str:
        if isinstance(data_batch, list) is False:
            raise ValueError("Invalid data format.")
        flow = 0
        for item in data_batch:
            if "buy" in item.lower():
                flow += int(item.split(":")[1])
            elif "sell" in item.lower():
                flow -= int(item.split(":")[1])
            else:
                raise ValueError("Invalid data format.")
        self.stats = len(data_batch)
        return f"Transaction analysis: {len(data_batch)} operations, net flow: {flow:+d} units"

    def filter_data(self, data_batch: List[Any]
                    , criteria: Optional[str] = None) -> List[Any]:
        if criteria == "large":
            fltrd = [item for item in data_batch if int(item.split(":")[1]) > 100]
            return fltrd
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"operations processed": self.stats}


class EventStream(DataStream):

    def __init__(self, stream_id):
        super().__init__(stream_id)
        self.stream_id = stream_id

    def process_batch(self, data_batch: List[Any]) -> str:
        if isinstance(data_batch, list) is False:
            raise ValueError("Invalid data format.")
        err = 0
        for item in data_batch:
            if "error" in item.lower():
                err += 1
        self.stats = len(data_batch)
        return f"Event analysis: {len(data_batch)} events, {err} errors detected"

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {"events processed": self.stats}


class StreamProcessor:

    def __init__(self):
        self.stream_list: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        self.stream_list.append(stream)

    def process_all(self, data_list: List[List[Any]]) -> None:
        data_type = ["Sensor", "Transaction", "Event"]
        for i in range(3):
            self.stream_list[i].process_batch(data_list[i])
            k, v = list(self.stream_list[i].get_stats().items())[0]
            print(f"- {data_type[i]} data: {v} {k}")

    def filter_all(self, data_list: List[List[Any]]) -> None:
        critical = len(self.stream_list[0].filter_data(data_list[0], "critical"))
        large = len(self.stream_list[1].filter_data(data_list[1], "large"))
        print(f"Filtered results: {critical} critical sensor alerts, "
              f"{large} large transaction")
    


def main():
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

    # ====== SENSOR STREAM ======
    print("\nInitializing Sensor Stream...")
    try:
        sensor = SensorStream("SENSOR_001")
        sensor_data = ["temp:", "humidity", "pressure:1013"]
        print(f"Stream ID: {sensor.stream_id}, Type: Environmental Data")
        print(f"Processing sensor batch: [{', '.join(sensor_data)}]")
        res = sensor.process_batch(sensor_data)
        print(res)

    except ValueError as e:
        print(f"Sensor analysis: [Error] {e}")

    # ====== TRANSACTION STREAM ======
    print("\nInitializing Transaction Stream...")
    try:
        trans = TransactionStream("TRANS_001")
        trans_data = ["buy:100", "sell:150", "buy:75"]
        print(f"Stream ID: {trans.stream_id}, Type: Financial Data")
        print(f"Processing transaction batch: [{', '.join(trans_data)}]")
        res = trans.process_batch(trans_data)
        print(res)

    except ValueError as e:
        print(f"Transaction analysis: [Error] {e}")

    # ====== EVENT STREAM ======
    print("\nInitializing Event Stream...")
    try:
        event = EventStream("EVENT_001")
        event_data = ["login", "error", "logout"]
        print(f"Stream ID: {event.stream_id}, Type: System Events")
        print(f"Processing event batch: [{', '.join(event_data)}]")
        res = event.process_batch(event_data)
        print(res)

    except ValueError as e:
        print(f"Event analysis: [Error] {e}")

    # ====== POLYMORPHIC STREAM ======
    print("\n=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...\n")
    strm = StreamProcessor()
    strm.add_stream(SensorStream("SENSOR_002"))
    strm.add_stream(TransactionStream("TRANS_002"))
    strm.add_stream(EventStream("EVENT_002"))
    print("Batch 1 results:")
    batch_1 = [
        ["temp:69", "temp:101"],
        ["buy:42", "sell:1337", "buy:22"],
        ["error", "login", "error"]
    ]
    try:
        strm.process_all(batch_1)
        print("\nStream filtering active: High-priority data only")
        strm.filter_all(batch_1)
        print("\nAll streams processed successfully. Nexus throughput optimal.")
    except ValueError as e:
        print(f"[ERROR] Stream processing failed. Details: {e}")


if __name__ == "__main__":
    main()
