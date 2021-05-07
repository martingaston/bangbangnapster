from src.payload_parser import parse_payload


def test_can_parse_a_napster_message():
    message = b'foo badpass 6699 "nap v0.8" 3'

    result = parse_payload(message)

    assert len(result) == 5
    assert result == ["foo", "badpass", "6699", "nap v0.8", "3"]


def test_can_parse_add_a_file_to_shared_file_index_payload():
    message = b'"generic band - generic song.mp3" b92870e0d41bc8e698cf2f0a1ddfeac7-443008 443332 128 44100 60'

    result = parse_payload(message)

    assert len(result) == 6
    assert result == [
        "generic band - generic song.mp3",
        "b92870e0d41bc8e698cf2f0a1ddfeac7-443008",
        "443332",
        "128",
        "44100",
        "60",
    ]
