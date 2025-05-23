from dataclasses import dataclass


@dataclass
class Score:
    perfects: int = 0
    greats: int = 0
    goods: int = 0
    misses: int = 0
    combo: int = 0
    max_combo: int = 0
    score: int = 0
    is_ap: bool = True
    is_fcplus: bool = True
    is_fc: bool = True
