from __future__ import annotations
from urllib.parse import urljoin
from dataclasses import dataclass
from typing import Optional, Union
from functools import reduce
import datetime as dt

import requests
import pandas as pd
import mplfinance as mpf

@dataclass
class TiingoRow:
    symbol: str
    date: dt.datetime
    close: float
    high: float
    low: float
    open: float
    volume: int
    adjClose: float
    adjHigh: float
    adjLow: float
    adjOpen: float
    adjVolume: int
    divCash: float
    splitFactor: float


class TiingoRequest:
    _base_url = "https://api.tiingo.com/tiingo/"
    def __init__(self,
                 symbol: str,
                 date_from: dt.datetime,
                 date_to: Optional[dt.datetime] = None,
                 resample_freq: Optional[str] = "daily") -> None:
        self.symbol = symbol
        self.date_from = date_from
        self.date_to = date_to
        self.resample_freq = resample_freq

    def get(self, token: str) -> list[TiingoRow]:
        _header = self._make_header(token)
        _args = [self.resample_freq + "/", self.symbol + "/", "prices/"]
        _payload = self._make_payload()
        full_url = reduce(urljoin, _args, self._base_url)
        response = requests.get(full_url, headers=_header, params=_payload)
        return self._row_factory(response.json())

    def _make_header(self, token: str) -> dict:
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + token
        }

    def _make_payload(self) -> dict:
        _payload = {
            "startDate": self.date_from,
            "resampleFreq": self.resample_freq
        }
        if self.date_to:
            _payload["endDate"] = self.date_to
        return _payload

    def _row_factory(self, _json: list[dict]) -> list[TiingoRow]:
        for row in _json:
            row["date"] = dt.datetime.strptime(row["date"],
                                               "%Y-%m-%dT%H:%M:%S.%fZ")
            row["symbol"] = self.symbol
        return [TiingoRow(**r) for r in _json]


def plot_candlestick(response: list[TiingoRow],
                     mav: Optional[Union[tuple, list]] = None,
                     volume: bool = False) -> None:
    symbol = response[0].symbol
    df = pd.DataFrame(response)
    df.set_index("date", inplace=True)
    df.columns = [column.capitalize() for column in df.columns]
    plot_kwargs = {
        "data": df,
        "volume": volume,
        "title": symbol
    }
    if mav:
        plot_kwargs["mav"] = mav
    mpf.plot(**plot_kwargs)