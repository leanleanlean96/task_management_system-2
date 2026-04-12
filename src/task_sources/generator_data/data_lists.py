from datetime import datetime

name_list: list[str] = [
    "Clear the goblin ambush",
    "Deliver the sealed letter",
    "Investigate the haunted crypt",
    "Escort the merchant caravan",
    "Retrieve the stolen relic",
]

description_list: list[str] = [
    "Travel to the location, deal with any threats, and report back to the quest giver.",
    "Venture into hostile territory and complete the task before nightfall.",
    "Gather your party, prepare supplies, and see the contract through to its end.",
    "Accept the commission from the guild and return once the work is done.",
    "Handle the matter discreetly and bring proof of completion to claim the reward.",
]

creation_date_list: list[datetime] = [
    datetime(2026, 3, 1, 10, 0),
    datetime(2026, 3, 1, 11, 0),
    datetime(2026, 3, 1, 12, 0),
    datetime(2026, 3, 1, 13, 0),
    datetime(2026, 3, 1, 14, 0),
]

completion_date_list: list[datetime | None] = [
    datetime(2026, 3, 10, 9, 0),
    datetime(2026, 3, 12, 15, 0),
    datetime(2026, 3, 15, 10, 0),
    datetime(2026, 3, 20, 17, 0),
    None,
]
