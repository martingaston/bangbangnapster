from src.payload_parser import parse_payload


def test_can_parse_a_napster_message():
    message = b'foo badpass 6699 "nap v0.8" 3'

    result = parse_payload(message)

    assert len(result) == 5
    assert result == ["foo", "badpass", "6699", "nap v0.8", "3"]
