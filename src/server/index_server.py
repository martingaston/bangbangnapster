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
        IndexServer.lock.acquire()
        IndexServer.list.append(IndexedFile(file, user))
        IndexServer.lock.release()

    def __len__(self):
        return len(IndexServer.list)

    def remove(self, file: File, user: User) -> None:
        IndexServer.lock.acquire()
        IndexServer.list.remove(IndexedFile(file, user))
        IndexServer.lock.release()

    def search(self, artist: str, title: str = "") -> List[IndexedFile]:
        if "'" in artist or "'" in title or '"' in artist or '"' in title:
            return []

        IndexServer.lock.acquire()
        result = [
            indexed_file
            for indexed_file in IndexServer.list
            if artist in indexed_file.file.filename
            and title in indexed_file.file.filename
        ]
        IndexServer.lock.release()

        return result
