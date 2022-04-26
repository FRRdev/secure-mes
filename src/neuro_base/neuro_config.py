from dataclasses import dataclass


@dataclass
class ConfigNNT:
    K: int = 3
    L: int = 5
    N: int = 16
