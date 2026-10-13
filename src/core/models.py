from dataclasses import dataclass
from datetime import datetime

@dataclass
class Tick:
    symbol: str
    timestamp: datetime
    ltp: float
    volume: int