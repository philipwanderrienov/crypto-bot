from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

import os

import requests
import urllib3

from app.domain.models.market import MarketCandle

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class BybitExchangeClient:
    def __init__(self) -> None:
        self._last_error: Optional[str] = None
        self._base_url = "https://api.bybit.com"
        self._proxies = self._load_proxies()

    def _load_proxies(self) -> Optional[dict]:
        http_proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
        https_proxy = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")

        proxies = {}
        if http_proxy:
            proxies["http"] = http_proxy
        if https_proxy:
            proxies["https"] = https_proxy

        return proxies or None

    def get_latest_candle(self, symbol: str, timeframe: str) -> MarketCandle:
        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": timeframe,
            "limit": 1,
        }

        try:
            response = requests.get(
                f"{self._base_url}/v5/market/kline",
                params=params,
                timeout=10,
                verify=False,
                proxies=self._proxies,
            )

            if response.status_code != 200:
                raise RuntimeError(f"Bybit HTTP {response.status_code}: {response.text[:300]}")

            try:
                payload = response.json()
            except Exception as exc:
                raise RuntimeError(f"Bybit returned non-JSON response: {response.text[:300]}") from exc

            if payload.get("retCode") != 0:
                raise RuntimeError(payload.get("retMsg", "Unknown Bybit API error"))

            rows = payload.get("result", {}).get("list", [])
            if not rows:
                raise RuntimeError("No kline data returned from Bybit")

            row = rows[0]
            open_time = datetime.fromtimestamp(int(row[0]) / 1000, tz=timezone.utc)
            return MarketCandle(
                symbol=symbol,
                timeframe=timeframe,
                open_time=open_time,
                open_price=float(row[1]),
                high_price=float(row[2]),
                low_price=float(row[3]),
                close_price=float(row[4]),
                volume=float(row[5]),
            )
        except Exception as exc:
            self._last_error = str(exc)
            raise RuntimeError(f"Failed to fetch Bybit market data: {exc}") from exc

    def get_last_error(self) -> Optional[str]:
        return self._last_error
