from enum import Enum


class IssueType(Enum):
    to_int = 3
    to_byte = b'0x3'
    fee = int(1e8)


class TransferType(Enum):
    to_int = 4
    to_byte = b'0x4'
    fee = int(1e5)


class ReissueType(Enum):
    to_int = 5
    to_byte = b'0x5'
    fee = int(1e5)


class BurnType(Enum):
    to_int = 6
    to_byte = b'0x6'
    fee = int(1e5)


class MatcherType(Enum):
    to_int = 7
    to_byte = b'0x7'
    fee = int(1e5)


class LeaseType(Enum):
    to_int = 8
    to_byte = b'0x8'
    fee = int(1e5)


class CancelLeaseType(Enum):
    to_int = 9
    to_byte = b'0x9'
    fee = int(1e5)


class AliasType(Enum):
    to_int = 10
    to_byte = b'0xa'
    mount = b'\x02'
    fee = int(1e5)


class MassType(Enum):
    to_int = 11
    to_byte = b'0xb'
    fee = int(5e4)
