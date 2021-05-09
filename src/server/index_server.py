from typing import List
import threading
from src.server.file import File
from src.server.user import User
from dataclasses import dataclass


@dataclass
class IndexedFile:
    file: File
    user: User

    def __repr__(self) -> str:
        return f'"{self.file.filename}" {self.file.md5} {self.file.size_in_bytes} {self.file.bitrate} {self.file.frequency} {self.file.time} {self.user.nick} {self.user.ip} {self.user.link_type.value}'


class IndexServer:
    list: List[IndexedFile] = []
    lock = threading.Lock()

    def __init__(self):
        pass

    def add(self, file: File, user: User) -> None:
        with IndexServer.lock:
            IndexServer.list.append(IndexedFile(file, user))

    def __len__(self):
        return len(IndexServer.list)

    def remove(self, file: File, user: User) -> None:
        with IndexServer.lock:
            IndexServer.list.remove(IndexedFile(file, user))

    def remove_all(self, user: User) -> int:
        with IndexServer.lock:
            before = len(IndexServer.list)
            new_list = [item for item in IndexServer.list if item.user != user]
            IndexServer.list = new_list
            after = len(IndexServer.list)

        return before - after

    def search(self, artist: str, title: str = "") -> List[IndexedFile]:
        if "'" in artist or "'" in title or '"' in artist or '"' in title:
            return []

        with IndexServer.lock:
            result = [
                indexed_file
                for indexed_file in IndexServer.list
                if artist in indexed_file.file.filename
                and title in indexed_file.file.filename
            ]

        return result
