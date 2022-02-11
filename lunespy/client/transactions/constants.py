from lunespy.utils import lunes_to_unes
from enum import Enum


class IssueType(Enum):
    to_int = 3
    to_byte = b'\x03'
    fee = lunes_to_unes(1)


class TransferType(Enum):
    to_int = 4
    to_byte = b'\x04'
    fee = lunes_to_unes(0.01)


class ReissueType(Enum):
    to_int = 5
    to_byte = b'\x05'
    fee = lunes_to_unes(0.01)


class BurnType(Enum):
    to_int = 6
    to_byte = b'\x06'
    fee = lunes_to_unes(0.01)


class LunexType(Enum):
    to_int = 7
    to_byte = b'\x07'
    fee = lunes_to_unes(0.01)


class LeaseType(Enum):
    to_int = 8
    to_byte = b'\x08'
    fee = lunes_to_unes(0.01)


class CancelLeaseType(Enum):
    to_int = 9
    to_byte = b'\x09'
    fee = lunes_to_unes(0.01)


class AliasType(Enum):
    to_int = 10
    to_byte = b'\x0a'
    mount = b'\x02'
    fee = lunes_to_unes(0.01)


class MassType(Enum):
    to_int = 11
    to_byte = b'\x0b'
    fee = lunes_to_unes(0.005)
