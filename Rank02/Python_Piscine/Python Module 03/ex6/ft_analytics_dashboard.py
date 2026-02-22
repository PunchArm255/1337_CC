#!/usr/bin/env python3
"""Data Alchemist: analytics dashboard using comprehensions."""


def get_game_data() -> dict:
    """Return the raw game data."""
    return {
        "players": {
            "alice": {
                "level": 41,
                "total_score": 2824,
                "sessions_played": 13,
                "favorite_mode": "ranked",
                "achievements_count": 5,
            },
            "bob": {
                "level": 16,
                "total_score": 4657,
                "sessions_played": 27,
                "favorite_mode": "ranked",
                "achievements_count": 2,
            },
            "charlie": {
                "level": 44,
                "total_score": 9935,
                "sessions_played": 21,
                "favorite_mode": "ranked",
                "achievements_count": 7,
            },
            "diana": {
                "level": 3,
                "total_score": 1488,
                "sessions_played": 21,
                "favorite_mode": "casual",
                "achievements_count": 4,
            },
            "eve": {
                "level": 33,
                "total_score": 1434,
                "sessions_played": 81,
                "favorite_mode": "casual",
                "achievements_count": 7,
            },
            "frank": {
                "level": 15,
                "total_score": 8359,
                "sessions_played": 85,
                "favorite_mode": "competitive",
                "achievements_count": 1,
            },
        },
        "sessions": [
            {
                "player": "bob",
                "duration_minutes": 94,
                "score": 1831,
                "mode": "competitive",
                "completed": False,
            },
            {
                "player": "bob",
                "duration_minutes": 32,
                "score": 1478,
                "mode": "casual",
                "completed": True,
            },
            {
                "player": "diana",
                "duration_minutes": 17,
                "score": 1570,
                "mode": "competitive",
                "completed": False,
            },
            {
                "player": "alice",
                "duration_minutes": 98,
                "score": 1981,
                "mode": "ranked",
                "completed": True,
            },
            {
                "player": "diana",
                "duration_minutes": 15,
                "score": 2361,
                "mode": "competitive",
                "completed": False,
            },
            {
                "player": "eve",
                "duration_minutes": 29,
                "score": 2985,
                "mode": "casual",
                "completed": True,
            },
            {
                "player": "frank",
                "duration_minutes": 34,
                "score": 1285,
                "mode": "casual",
                "completed": True,
            },
            {
                "player": "alice",
                "duration_minutes": 53,
                "score": 1238,
                "mode": "competitive",
                "completed": False,
            },
            {
                "player": "bob",
                "duration_minutes": 52,
                "score": 1555,
                "mode": "casual",
                "completed": False,
            },
            {
                "player": "frank",
                "duration_minutes": 92,
                "score": 2754,
                "mode": "casual",
                "completed": True,
            },
            {
                "player": "eve",
                "duration_minutes": 98,
                "score": 1102,
                "mode": "casual",
                "completed": False,
            },
            {
                "player": "diana",
                "duration_minutes": 39,
                "score": 2721,
                "mode": "ranked",
                "completed": True,
            },
            {
                "player": "frank",
                "duration_minutes": 46,
                "score": 329,
                "mode": "casual",
                "completed": True,
            },
            {
                "player": "charlie",
                "duration_minutes": 56,
                "score": 1196,
                "mode": "casual",
                "completed": True,
            },
            {
                "player": "eve",
                "duration_minutes": 117,
                "score": 1388,
                "mode": "casual",
                "completed": False,
            },
            {
                "player": "diana",
                "duration_minutes": 118,
                "score": 2733,
                "mode": "competitive",
                "completed": True,
            },
            {
                "player": "charlie",
                "duration_minutes": 22,
                "score": 1110,
                "mode": "ranked",
                "completed": False,
            },
            {
                "player": "frank",
                "duration_minutes": 79,
                "score": 1854,
                "mode": "ranked",
                "completed": False,
            },
            {
                "player": "charlie",
                "duration_minutes": 33,
                "score": 666,
                "mode": "ranked",
                "completed": False,
            },
            {
                "player": "alice",
                "duration_minutes": 101,
                "score": 292,
                "mode": "casual",
                "completed": True,
            },
            {
                "player": "frank",
                "duration_minutes": 25,
                "score": 2887,
                "mode": "competitive",
                "completed": True,
            },
            {
                "player": "diana",
                "duration_minutes": 53,
                "score": 2540,
                "mode": "competitive",
                "completed": False,
            },
            {
                "player": "eve",
                "duration_minutes": 115,
                "score": 147,
                "mode": "ranked",
                "completed": True,
            },
            {
                "player": "frank",
                "duration_minutes": 118,
                "score": 2299,
                "mode": "competitive",
                "completed": False,
            },
            {
                "player": "alice",
                "duration_minutes": 42,
                "score": 1880,
                "mode": "casual",
                "completed": False,
            },
            {
                "player": "alice",
                "duration_minutes": 97,
                "score": 1178,
                "mode": "ranked",
                "completed": True,
            },
            {
                "player": "eve",
                "duration_minutes": 18,
                "score": 2661,
                "mode": "competitive",
                "completed": True,
            },
            {
                "player": "bob",
                "duration_minutes": 52,
                "score": 761,
                "mode": "ranked",
                "completed": True,
            },
            {
                "player": "eve",
                "duration_minutes": 46,
                "score": 2101,
                "mode": "casual",
                "completed": True,
            },
            {
                "player": "charlie",
                "duration_minutes": 117,
                "score": 1359,
                "mode": "casual",
                "completed": True,
            },
        ],
        "game_modes": ["casual", "competitive", "ranked"],
        "achievements": ["first_blood", "level_master", "speed_runner"],
    }


def main() -> None:
    """Run list, dict, and set comprehension analytics."""
    game_data = get_game_data()
    players = game_data["players"]
    sessions = game_data["sessions"]
    modes = game_data["game_modes"]
    achievements = game_data["achievements"]

    print("=== Game Analytics Dashboard ===\n")

    print("=== List Comprehension Examples ===")
    hi_scorers = list({x["player"] for x in sessions if x["score"] > 2000})
    doubled = [x["total_score"] * 2 for x in players.values()]
    active = [
        name for name, stat in players.items() if stat["sessions_played"] > 20
    ]
    print(f"High scorers (>2000): {hi_scorers}")
    print(f"Scores doubled: {doubled}")
    print(f"Active players: {active}")

    print("\n=== Dict Comprehension Examples ===")
    scores = {name: stat["total_score"] for name, stat in players.items()}
    cat_scores = {
        "high": len(
            {
                x["total_score"]
                for x in players.values()
                if x["total_score"] > 5000
            }
        ),
        "medium": len(
            {
                x["total_score"]
                for x in players.values()
                if 3000 < x["total_score"] < 5000
            }
        ),
        "low": len(
            {
                x["total_score"]
                for x in players.values()
                if x["total_score"] < 3000
            }
        ),
    }
    achievs = {
        name: stat["achievements_count"] for name, stat in players.items()
    }
    print(f"Player scores: {scores}")
    print(f"Score categories: {cat_scores}")
    print(f"Achievement counts: {achievs}")

    print("\n=== Set Comprehension Examples ===")
    u_players = {x["player"] for x in sessions}
    u_achiev = {x for x in achievements}
    u_modes = {x for x in modes}

    print(f"Unique players: {u_players}")
    print(f"Unique achievements: {u_achiev}")
    print(f"Unique game modes: {u_modes}")

    print("\n=== Combined Analysis ===")
    avg_score = sum(
        [stat["total_score"] for name, stat in players.items()]
    ) / len(u_players)
    top_name, top_score, top_achievs = "", -1, 0

    for name, stat in players.items():
        if stat["total_score"] > top_score:
            top_score = stat["total_score"]
            top_name = name
            top_achievs = stat["achievements_count"]

    print(f"Total players: {len(u_players)}")
    print(f"Total unique achievements: {len(u_achiev)}")
    print(f"Average score: {avg_score:.1f}")
    print(
        f"Top performer: {top_name} ({top_score} points, {top_achievs} "
        "achievements)"
    )


if __name__ == "__main__":
    main()
