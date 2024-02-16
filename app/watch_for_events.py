import random
from time import sleep

event_weights = {
    "⚽ Goooal!!!": 10,
    "Penalty!! Shot and... he missed it.": 8,
    "⚽ Penalty!! Shot and... he scored!!": 8,
    "This is a deserved red card after a very rough tackle on the player": 6,
    "Foul, the referee is reaching for his pocket, and it's a red card for!": 4,
    "The goalkeeper saves, and it's a corner.": 3,
    "Corner from left side": 2,
    "Corner from right side": 2,
    "Close-range shot and a save! ": 2,
    "Ball is out of the pitch": 1,
    "Shot from great position but blocked in last moment": 1,
    "Shot from distance but wide from target": 1,
    "Great save from goalkeeper": 1,
}


def watch_for_events():
    event_types = list(event_weights.keys())
    weights = list(event_weights.values())

    yield "event: started\ndata: Game has started!\n\n"

    for ticker in range(0, 90):
        if random.choices([True, False], weights=[0.1, 0.9], k=1)[0]:
            event = random.choices(event_types, weights=weights, k=1)[0]
            yield f"data: {ticker}min {event}\n\n"
            sleep(1)
        if ticker == 45:
            yield "event: halftime\ndata: Half-time!\n\n"

    yield f"event: finished\ndata: The referee's whistle, and the end of the match.\n\n"
