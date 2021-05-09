import pytest
from src.server.index_server import IndexServer
from src.server.file import File
from src.server.user import User


@pytest.fixture
def index_server():
    index_server = IndexServer()
    IndexServer.list = []

    return index_server


def test_an_index_server_with_no_files_has_a_length_of_zero(index_server) -> None:

    assert len(index_server) == 0


def test_can_add_a_file_to_the_index_server(index_server) -> None:
    file = None
    user = None

    index_server.add(file, user)

    assert len(index_server) == 1


def test_can_remove_a_file_from_the_index_server(index_server):
    file1, user1 = None, None
    file2, user2 = None, None
    index_server.add(file1, user1)
    index_server.add(file2, user2)

    index_server.remove(file2, user2)

    assert len(index_server) == 1


def test_cannot_remove_a_file_that_does_not_exist_in_the_server(index_server):
    file, user = None, None
    file_not_on_index_server = 1
    index_server.add(file, user)

    with pytest.raises(ValueError):
        index_server.remove(file_not_on_index_server, user)


def test_can_search_the_index_server(index_server):
    file = File("generic band - generic song.mp3", "abcd", 1234, 128, 44100, 120)
    user = User("foobar2000", "abcd", 12345, 6600, "napster", 6)
    index_server.add(file, user)

    [result] = index_server.search("generic band", "generic song")

    assert result.file == file
    assert result.user == user


def test_can_search_the_index_server_with_multiple_results(index_server):
    file1 = File("generic band - generic song.mp3", "abcd", 1234, 128, 44100, 120)
    file2 = File(
        "generic band - difficult followup to generic song.mp3",
        "abcd",
        1234,
        128,
        44100,
        120,
    )
    user1 = User("foobar2000", "abcd", 12345, 6600, "napster", 6)

    index_server.add(file1, user1)
    index_server.add(file2, user1)

    [result1, result2] = index_server.search("generic band", "generic song")

    assert result1.file == file1
    assert result1.user == user1
    assert result2.file == file2
    assert result2.user == user1


def test_cannot_search_with_a_quoted_string(index_server) -> None:
    file = File("generic band - generic song.mp3", "abcd", 1234, 128, 44100, 120)
    user = User("foobar2000", "abcd", 12345, 6600, "napster", 6)

    index_server.add(file, user)

    result = index_server.search("generic 'fun' band")

    assert result == []
