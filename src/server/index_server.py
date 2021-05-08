from typing import List
from src.server.file import File
from src.server.user import User
from dataclasses import dataclass


@dataclass
class IndexedFile:
    file: File
    user: User


class IndexServer:
    def __init__(self):
        self.list: List[IndexedFile] = []

    def add(self, file: File, user: User) -> None:
        self.list.append(IndexedFile(file, user))

    def __len__(self):
        return len(self.list)

    def remove(self, file: File, user: User) -> None:
        self.list.remove(IndexedFile(file, user))

    def search(self, artist: str, title: str) -> List[IndexedFile]:
        result = [
            indexed_file
            for indexed_file in self.list
            if artist in indexed_file.file.filename
            and title in indexed_file.file.filename
        ]

        return result
