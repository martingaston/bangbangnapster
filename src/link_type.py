from enum import Enum


class LinkType(Enum):
    UNKNOWN = 0
    MODEM_14K = 1
    MODEM_28K = 2
    MODEM_33K = 3
    MODEM_56K = 4
    ISDN_64K = 5
    ISDN_128K = 6
    CABLE = 7
    DSL = 8
    T1 = 9
    T3_OR_GREATER = 10
