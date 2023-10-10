from enum import Enum
from decimal import Decimal
from datetime import datetime
from pydantic.dataclasses import dataclass

class Side(Enum):
    BUY = "buy"
    SELL = "sell"

class Timeframe(Enum):
    MINUTLY = "1m"
    HOURLY = "1h"
    DAILY = "1d"
    WEEKLY = "1w"
    MONTHLY = "1M"

@dataclass
class Trade:
    time: datetime
    side: Side
    price: Decimal
    volume: Decimal

@dataclass
class Candle:
    time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal

@dataclass
class Ticker:
    symbol: str
    price: Decimal
    volume: Decimal