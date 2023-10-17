from .models import Candle

def verify_candle(candle: Candle) -> bool:
    ishighest = candle.high == max(candle.high, candle.low, candle.open, candle.close)
    islowest = candle.low == min(candle.high, candle.low, candle.open, candle.close)
    return  ishighest and islowest