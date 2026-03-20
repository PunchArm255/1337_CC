#!/usr/bin/env python3
"""Stream Wizard: memory-efficient data processing with generators."""


import time
from typing import Generator


def get_raw_data() -> list[dict]:
    """Return the raw list of game event data."""
    return [
        {
            "id": 1,
            "player": "frank",
            "event_type": "login",
            "timestamp": "2024-01-01T23:17",
            "data": {"level": 16, "score_delta": 128, "zone": "pixel_zone_2"},
        },
        {
            "id": 2,
            "player": "frank",
            "event_type": "login",
            "timestamp": "2024-01-22T23:57",
            "data": {"level": 35, "score_delta": -11, "zone": "pixel_zone_5"},
        },
        {
            "id": 3,
            "player": "diana",
            "event_type": "login",
            "timestamp": "2024-01-01T02:13",
            "data": {"level": 15, "score_delta": 417, "zone": "pixel_zone_5"},
        },
        {
            "id": 4,
            "player": "alice",
            "event_type": "level_up",
            "timestamp": "2024-01-07T22:41",
            "data": {"level": 45, "score_delta": 458, "zone": "pixel_zone_4"},
        },
        {
            "id": 5,
            "player": "bob",
            "event_type": "death",
            "timestamp": "2024-01-19T08:51",
            "data": {"level": 1, "score_delta": 63, "zone": "pixel_zone_4"},
        },
        {
            "id": 6,
            "player": "charlie",
            "event_type": "kill",
            "timestamp": "2024-01-05T06:48",
            "data": {"level": 22, "score_delta": 4, "zone": "pixel_zone_1"},
        },
        {
            "id": 7,
            "player": "diana",
            "event_type": "login",
            "timestamp": "2024-01-12T11:38",
            "data": {"level": 17, "score_delta": -56, "zone": "pixel_zone_4"},
        },
        {
            "id": 8,
            "player": "eve",
            "event_type": "login",
            "timestamp": "2024-01-30T12:05",
            "data": {"level": 36, "score_delta": 200, "zone": "pixel_zone_5"},
        },
        {
            "id": 9,
            "player": "charlie",
            "event_type": "level_up",
            "timestamp": "2024-01-07T22:04",
            "data": {"level": 3, "score_delta": 133, "zone": "pixel_zone_3"},
        },
        {
            "id": 10,
            "player": "alice",
            "event_type": "logout",
            "timestamp": "2024-01-28T03:24",
            "data": {"level": 18, "score_delta": 364, "zone": "pixel_zone_3"},
        },
        {
            "id": 11,
            "player": "bob",
            "event_type": "kill",
            "timestamp": "2024-01-12T06:42",
            "data": {"level": 18, "score_delta": -27, "zone": "pixel_zone_5"},
        },
        {
            "id": 12,
            "player": "frank",
            "event_type": "logout",
            "timestamp": "2024-01-18T23:15",
            "data": {"level": 11, "score_delta": 373, "zone": "pixel_zone_4"},
        },
        {
            "id": 13,
            "player": "charlie",
            "event_type": "item_found",
            "timestamp": "2024-01-23T17:14",
            "data": {"level": 44, "score_delta": 232, "zone": "pixel_zone_1"},
        },
        {
            "id": 14,
            "player": "bob",
            "event_type": "login",
            "timestamp": "2024-01-26T10:25",
            "data": {"level": 18, "score_delta": -33, "zone": "pixel_zone_2"},
        },
        {
            "id": 15,
            "player": "eve",
            "event_type": "item_found",
            "timestamp": "2024-01-11T06:41",
            "data": {"level": 32, "score_delta": 305, "zone": "pixel_zone_4"},
        },
        {
            "id": 16,
            "player": "bob",
            "event_type": "kill",
            "timestamp": "2024-01-05T07:47",
            "data": {"level": 36, "score_delta": 451, "zone": "pixel_zone_3"},
        },
        {
            "id": 17,
            "player": "frank",
            "event_type": "level_up",
            "timestamp": "2024-01-14T18:25",
            "data": {"level": 24, "score_delta": 124, "zone": "pixel_zone_2"},
        },
        {
            "id": 18,
            "player": "eve",
            "event_type": "death",
            "timestamp": "2024-01-03T01:55",
            "data": {"level": 8, "score_delta": 56, "zone": "pixel_zone_2"},
        },
        {
            "id": 19,
            "player": "frank",
            "event_type": "death",
            "timestamp": "2024-01-20T02:24",
            "data": {"level": 25, "score_delta": 379, "zone": "pixel_zone_5"},
        },
        {
            "id": 20,
            "player": "charlie",
            "event_type": "level_up",
            "timestamp": "2024-01-28T00:43",
            "data": {"level": 47, "score_delta": 17, "zone": "pixel_zone_5"},
        },
        {
            "id": 21,
            "player": "charlie",
            "event_type": "item_found",
            "timestamp": "2024-01-11T03:18",
            "data": {"level": 28, "score_delta": 61, "zone": "pixel_zone_4"},
        },
        {
            "id": 22,
            "player": "alice",
            "event_type": "item_found",
            "timestamp": "2024-01-29T23:16",
            "data": {"level": 33, "score_delta": 82, "zone": "pixel_zone_5"},
        },
        {
            "id": 23,
            "player": "alice",
            "event_type": "item_found",
            "timestamp": "2024-01-10T20:32",
            "data": {"level": 39, "score_delta": 103, "zone": "pixel_zone_2"},
        },
        {
            "id": 24,
            "player": "charlie",
            "event_type": "logout",
            "timestamp": "2024-01-18T16:58",
            "data": {"level": 1, "score_delta": 231, "zone": "pixel_zone_4"},
        },
        {
            "id": 25,
            "player": "alice",
            "event_type": "login",
            "timestamp": "2024-01-30T11:56",
            "data": {"level": 20, "score_delta": 145, "zone": "pixel_zone_1"},
        },
        {
            "id": 26,
            "player": "bob",
            "event_type": "level_up",
            "timestamp": "2024-01-03T02:46",
            "data": {"level": 32, "score_delta": -30, "zone": "pixel_zone_5"},
        },
        {
            "id": 27,
            "player": "bob",
            "event_type": "logout",
            "timestamp": "2024-01-22T15:35",
            "data": {"level": 11, "score_delta": 171, "zone": "pixel_zone_5"},
        },
        {
            "id": 28,
            "player": "eve",
            "event_type": "death",
            "timestamp": "2024-01-07T17:48",
            "data": {"level": 47, "score_delta": 105, "zone": "pixel_zone_3"},
        },
        {
            "id": 29,
            "player": "diana",
            "event_type": "item_found",
            "timestamp": "2024-01-21T11:28",
            "data": {"level": 34, "score_delta": 362, "zone": "pixel_zone_1"},
        },
        {
            "id": 30,
            "player": "bob",
            "event_type": "logout",
            "timestamp": "2024-01-03T10:01",
            "data": {"level": 38, "score_delta": 467, "zone": "pixel_zone_2"},
        },
        {
            "id": 31,
            "player": "eve",
            "event_type": "logout",
            "timestamp": "2024-01-01T02:45",
            "data": {"level": 41, "score_delta": -40, "zone": "pixel_zone_2"},
        },
        {
            "id": 32,
            "player": "alice",
            "event_type": "login",
            "timestamp": "2024-01-28T10:04",
            "data": {"level": 33, "score_delta": 143, "zone": "pixel_zone_3"},
        },
        {
            "id": 33,
            "player": "frank",
            "event_type": "death",
            "timestamp": "2024-01-07T17:08",
            "data": {"level": 47, "score_delta": 484, "zone": "pixel_zone_5"},
        },
        {
            "id": 34,
            "player": "diana",
            "event_type": "logout",
            "timestamp": "2024-01-26T15:51",
            "data": {"level": 27, "score_delta": 94, "zone": "pixel_zone_1"},
        },
        {
            "id": 35,
            "player": "alice",
            "event_type": "item_found",
            "timestamp": "2024-01-14T11:27",
            "data": {"level": 27, "score_delta": 378, "zone": "pixel_zone_1"},
        },
        {
            "id": 36,
            "player": "frank",
            "event_type": "item_found",
            "timestamp": "2024-01-21T03:03",
            "data": {"level": 26, "score_delta": 247, "zone": "pixel_zone_1"},
        },
        {
            "id": 37,
            "player": "bob",
            "event_type": "logout",
            "timestamp": "2024-01-07T17:28",
            "data": {"level": 9, "score_delta": 332, "zone": "pixel_zone_2"},
        },
        {
            "id": 38,
            "player": "charlie",
            "event_type": "death",
            "timestamp": "2024-01-08T02:28",
            "data": {"level": 36, "score_delta": 0, "zone": "pixel_zone_1"},
        },
        {
            "id": 39,
            "player": "frank",
            "event_type": "level_up",
            "timestamp": "2024-01-27T00:05",
            "data": {"level": 49, "score_delta": 142, "zone": "pixel_zone_2"},
        },
        {
            "id": 40,
            "player": "diana",
            "event_type": "death",
            "timestamp": "2024-01-16T06:55",
            "data": {"level": 26, "score_delta": -40, "zone": "pixel_zone_2"},
        },
        {
            "id": 41,
            "player": "diana",
            "event_type": "login",
            "timestamp": "2024-01-13T08:59",
            "data": {"level": 30, "score_delta": 192, "zone": "pixel_zone_4"},
        },
        {
            "id": 42,
            "player": "frank",
            "event_type": "item_found",
            "timestamp": "2024-01-26T17:42",
            "data": {"level": 46, "score_delta": 398, "zone": "pixel_zone_2"},
        },
        {
            "id": 43,
            "player": "bob",
            "event_type": "kill",
            "timestamp": "2024-01-07T01:37",
            "data": {"level": 48, "score_delta": 455, "zone": "pixel_zone_1"},
        },
        {
            "id": 44,
            "player": "frank",
            "event_type": "kill",
            "timestamp": "2024-01-02T01:37",
            "data": {"level": 31, "score_delta": 414, "zone": "pixel_zone_5"},
        },
        {
            "id": 45,
            "player": "bob",
            "event_type": "login",
            "timestamp": "2024-01-17T02:54",
            "data": {"level": 12, "score_delta": -30, "zone": "pixel_zone_5"},
        },
        {
            "id": 46,
            "player": "alice",
            "event_type": "item_found",
            "timestamp": "2024-01-28T07:25",
            "data": {"level": 8, "score_delta": 483, "zone": "pixel_zone_2"},
        },
        {
            "id": 47,
            "player": "eve",
            "event_type": "level_up",
            "timestamp": "2024-01-02T19:05",
            "data": {"level": 27, "score_delta": 497, "zone": "pixel_zone_5"},
        },
        {
            "id": 48,
            "player": "eve",
            "event_type": "kill",
            "timestamp": "2024-01-30T08:13",
            "data": {"level": 43, "score_delta": 221, "zone": "pixel_zone_2"},
        },
        {
            "id": 49,
            "player": "charlie",
            "event_type": "death",
            "timestamp": "2024-01-05T21:41",
            "data": {"level": 20, "score_delta": 368, "zone": "pixel_zone_3"},
        },
        {
            "id": 50,
            "player": "alice",
            "event_type": "login",
            "timestamp": "2024-01-15T19:36",
            "data": {"level": 7, "score_delta": -25, "zone": "pixel_zone_5"},
        },
    ]


def game_gen(n: int) -> Generator[str, None, None]:
    """Yield formatted game event strings from raw data."""

    raw_data = get_raw_data()

    for i in range(n):
        item = raw_data[i % len(raw_data)]

        event = (
            f"Event {i}: Player {item['player']} "
            f"(level {item['data']['level']}) {item['event_type']}"
        )
        yield event


def fibo_gen(n: int) -> Generator[int, None, None]:
    """Yield the first n Fibonacci numbers."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, b + a


def prime_gen(n: int) -> Generator[int, None, None]:
    """Yield the first n prime numbers."""
    count = 0
    x = 2

    while count < n:
        is_prime = True
        for i in range(2, x):
            if x % i == 0:
                is_prime = False
                break
        if is_prime:
            yield x
            count += 1
        x += 1


def main() -> None:
    """Process game event streams and display analytics."""
    print("=== Game Data Stream Processor ===\n")

    total_events = 1000
    tres_event = 0
    lvlup_event = 0
    high_lvl = 0
    raw_data = get_raw_data()

    start_time = time.time()

    print(f"Processing {total_events} game events...\n")

    for event in game_gen(total_events):
        if "Event 1:" in event or "Event 2:" in event or "Event 3: " in event:
            print(event)
        if "item_found" in event:
            tres_event += 1
        if "level_up" in event:
            lvlup_event += 1

    for i in range(len(raw_data)):
        element = raw_data[i]
        if element["data"]["level"] >= 10:
            high_lvl += 1

    end_time = time.time()
    proc_time = end_time - start_time

    print("...")
    print("\n=== Stream Analytics ===")
    print(f"Total events processed: {total_events}")
    print(f"High-level players (10+): {high_lvl}")
    print(f"Treasure events: {tres_event}")
    print(f"Level-up events: {lvlup_event}")
    print("\nMemory usage: Constant (streaming)")
    print(f"Processing time: {proc_time:.3f} seconds")

    print("\n=== Generator Demonstration ===")
    fib = [str(x) for x in fibo_gen(10)]
    prime = [str(x) for x in prime_gen(5)]
    print(f"Fibonacci sequence (first 10): {', '.join(fib)}")
    print(f"Prime numbers (first 5): {', '.join(prime)}")


if __name__ == "__main__":
    main()
