from typing import List


def parse_payload(data: bytes) -> List[str]:
    parsed = []

    in_string = False
    last_char_was_end_of_string = False
    current = []

    # concatenating a space at the end means we finish by pushing the final item in current to the parsed list
    for x in data.decode("ascii") + " ":
        if last_char_was_end_of_string:
            last_char_was_end_of_string = False
            continue

        if in_string and x == '"':
            parsed.append("".join(current))
            in_string = False
            last_char_was_end_of_string = True
            current = []
            continue

        if in_string:
            current.append(x)
            continue

        if x == '"':
            in_string = True
            continue

        if x == " ":
            parsed.append("".join(current))
            current = []
            continue

        current.append(x)

    return parsed
