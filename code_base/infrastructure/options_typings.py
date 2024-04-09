from enum import Enum


class PayoffType(Enum):
    Call = 0
    Put = 1
    BinaryCall = 2
    BinaryPut = 3
