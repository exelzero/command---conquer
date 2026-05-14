import random

ANIME_NAMES = [
    "GOJO", "DEKU", "BAKU", "TOGA", "DABI", "HAWK",
    "TOGE", "YUJI", "DOMA", "ZENI", "RENG", "NEZU",
    "ASTA", "YUNO", "NERO", "TANJ", "KIRI", "IIDA",
    "GOKU", "ZORO", "NAMI", "LEVI", "EREN", "YMIR",
    "REVY", "HIEI", "MAKA", "SOUL", "FAYE", "RIZA",
]

_assigned = set()


def assign_name() -> str:
    available = [n for n in ANIME_NAMES if n not in _assigned]
    if not available:
        raise RuntimeError("Peon name pool exhausted")
    name = random.choice(available)
    _assigned.add(name)
    return name


def release_name(name: str):
    _assigned.discard(name)


def assigned_names() -> list:
    return list(_assigned)
