from enum import Enum


class PacketType(Enum):
    LOGOUT_OR_ERROR_MESSAGE_FROM_SERVER = 0x00
    REGISTERED_LOGIN_REQUEST = 0x02
    LOGIN_ACKNOWLEDGE = 0x03
    ADD_A_FILE_TO_SHARED_FILE_INDEX = 0x64
    SEARCH_QUERY_REQUEST = 0xC8
    SEARCH_QUERY_RESULTS = 0xC9
    SEARCH_QUERY_RESULTS_END_NOTIFICATION = 0xCA
