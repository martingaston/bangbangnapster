from enum import Enum


class PacketType(Enum):
    REGISTERED_LOGIN_REQUEST = 0x02
    ADD_A_FILE_TO_SHARED_FILE_INDEX = 0x64
