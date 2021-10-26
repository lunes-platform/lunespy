from enum import Enum


class IssueType(Enum):
    type_int = 3
    type_byte = b'0x3'
    fee = int(1e8)


class TransferType(Enum):
    type_int = 4
    type_byte = b'0x4'
    fee = int(1e5)


class ReissueType(Enum):
    type_int = 5
    type_byte = b'0x5'
    fee = int(1e5)


class BurnType(Enum):
    type_int = 6
    type_byte = b'0x6'
    fee = int(1e5)


class MatcherType(Enum):
    type_int = 7
    type_byte = b'0x7'
    fee = int(1e5)


class LeaseType(Enum):
    type_int = 8
    type_byte = b'0x8'
    fee = int(1e5)


class CancelLeaseType(Enum):
    type_int = 9
    type_byte = b'0x9'
    fee = int(1e5)


class AliasType(Enum):
    type_int = 10
    type_byte = b'0xa'
    mount = b'\x02'
    fee = int(1e5)


class MassType(Enum):
    type_int = 11
    type_byte = b'0xb'
    fee = int(5e4)
