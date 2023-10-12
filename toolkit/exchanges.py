import httpx

from os import environ
from .models import Timeframe, Trade, Candle, Ticker

class Coinalyze():
    BASEURL = "https://api.coinalyze.net"
    ENDPOINTS = {
        "spot": "/v1/spot-markets",
        "future": "/v1/future-markets",
        "openinterest": "/v1/open-interest",
        "funding": "/v1/funding-rate"
    }

    def __init__(self) -> None:
        self.key = environ.get("COINALYZE", "")
        if self.key == "":
            raise KeyError("You need to provide a Coinalyze API key in a COINALYZE env variable!")
        
    def spot_markets(self):
        url = Coinalyze.BASEURL + Coinalyze.ENDPOINTS["spot"]
        headers = {"api_key" : self.key}
        r = httpx.get(url, headers=headers)

        if r.status_code != httpx.codes.OK:
            raise httpx.HTTPError(r.json())
        
        return r.json()

    def futures_markets(self):
        url = Coinalyze.BASEURL + Coinalyze.ENDPOINTS["future"]
        headers = {"api_key" : self.key}
        r = httpx.get(url, headers=headers)

        if r.status_code != httpx.codes.OK:
            raise httpx.HTTPError(r.json())
        
        return r.json()
        
    def open_interest(self, markets: list[str]):
        if len(markets) > 20:
            raise Exception("Coinalyze imposes a maximum of 20 markets per request!")

        url = Coinalyze.BASEURL + Coinalyze.ENDPOINTS["openinterest"]
        headers = { "api_key" : self.key }
        payload = { "symbols": ",".join(markets), "convert_to_usd": "true" }
        r = httpx.get(url, headers=headers, params=payload)

        if r.status_code != httpx.codes.OK:
            raise httpx.HTTPError(r.json())
        
        return r.json()

    def funding(self, markets: list[str]):
        if len(markets) > 20:
            raise Exception("Coinalyze imposes a maximum of 20 markets per request!")

        url = Coinalyze.BASEURL + Coinalyze.ENDPOINTS["funding"]
        headers = { "api_key" : self.key }
        payload = { "symbols": ",".join(markets) }
        r = httpx.get(url, headers=headers, params=payload)

        if r.status_code != httpx.codes.OK:
            raise httpx.HTTPError(r.json())
        
        return r.json()

class Binance():
    BASEURL = "https://api.binance.com"
    FUTURES = "https://fapi.binance.com"
    ENDPOINTS = {
        "ticker": "/api/v3/ticker/24hr",
        "price": "/api/v3/ticker/price",
        "kline": "/api/v3/klines",
        "trade": "/api/v3/trades"
    }

    def __init__(self) -> None:
        pass

    def _ds(self, ismaker: bool) -> str:
        """Determines if a given trade was a buy or sell order."""
        if ismaker:
            return "sell"
        else:
            return "buy"

    def markets(self) -> list[Ticker]:
        url = Binance.BASEURL + Binance.ENDPOINTS["ticker"]
        r = httpx.get(url)

        if r.status_code != httpx.codes.OK:
            raise httpx.HTTPError(r.json())

        return [Ticker(ticker["symbol"], ticker["lastPrice"], ticker["volume"]) for ticker in r.json()]
    
    async def trades(self, client: httpx.AsyncClient, symbol: str, limit: int = 500) -> list[Trade]:
        url = Binance.BASEURL + Binance.ENDPOINTS["trade"]
        payload = { "symbol": symbol, "limit": limit }
        r = httpx.get(url, params=payload)

        if r.status_code != httpx.codes.OK:
            raise httpx.HTTPError(r.json())
        
        return [Trade(trade["time"], self._ds(trade["isBuyerMaker"]), trade["price"], trade["qty"]) for trade in r.json()]

    async def kline(self, client: httpx.AsyncClient, symbol: str, interval: Timeframe, limit: int = 500) -> list[Candle]:
        url = Binance.BASEURL + Binance.ENDPOINTS["kline"]
        payload = { "symbol": symbol, "interval": interval.value, "limit": limit }
        r = await client.get(url, params=payload)

        if r.status_code != httpx.codes.OK:
            raise httpx.HTTPError(r.json())

        return [Candle(*kline[:6]) for kline in r.json()]