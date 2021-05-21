import secrets

feeling = [
    "plucky",
    "determined",
    "spirited",
    "distracted",
    "upset",
    "amused",
    "creative",
    "distraught",
    "sad",
    "upset",
    "miserable",
]

descriptor = [
    "young",
    "old",
    "tall",
    "little",
    "giant",
    "average",
    "weenie",
    "gargantuan",
]

colour = [
    "red",
    "blue",
    "yellow",
    "green",
    "orange",
    "cyan",
    "magenta",
    "teal",
    "purple",
    "pink",
    "blue",
]

animal = [
    "fox",
    "badger",
    "vixen",
    "mole",
    "weasel",
    "owl",
    "hedgehog",
    "pheasant",
    "toad",
    "adder",
    "kestrel",
]


def generate_username() -> str:
    return f"{secrets.choice(feeling)}-{secrets.choice(descriptor)}-{secrets.choice(colour)}-{secrets.choice(animal)}"
