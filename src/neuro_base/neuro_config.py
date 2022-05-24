from dataclasses import dataclass


@dataclass
class ConfigNNT:
    K: int = 5
    L: int = 5
    N: int = 16
