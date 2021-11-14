from enum import Enum


class IssueType(Enum):
    to_int = 3
    to_byte = b'\x03'
    fee = int(1e10)


class TransferType(Enum):
    to_int = 4
    to_byte = b'\x04'
    fee = int(1e5)


class ReissueType(Enum):
    to_int = 5
    to_byte = b'\x05'
    fee = int(1e5)


class BurnType(Enum):
    to_int = 6
    to_byte = b'\x06'
    fee = int(1e5)


class LunexType(Enum):
    to_int = 7
    to_byte = b'\x07'
    fee = int(1e5)


class LeaseType(Enum):
    to_int = 8
    to_byte = b'\x08'
    fee = int(1e5)


class CancelLeaseType(Enum):
    to_int = 9
    to_byte = b'\x09'
    fee = int(1e5)


class AliasType(Enum):
    to_int = 10
    to_byte = b'\x0a'
    mount = b'\x02'
    fee = int(1e5)


class MassType(Enum):
    to_int = 11
    to_byte = b'\x0b'
    fee = int(5e4)
