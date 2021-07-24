from __future__ import annotations
from argparse import ArgumentParser
import datetime as dt
import os

from tiingo import TiingoRequest, plot_candlestick


def main(token: str,
         symbol: str,
         date_from: dt.datetime,
         date_to: dt.datetime,
         mav: list,
         volume: bool) -> None:
    request = TiingoRequest(symbol=symbol,
                            date_from=date_from,
                            date_to=date_to)
    response = request.get(token=token)
    plot_candlestick(response, mav=mav, volume=volume)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    token = os.environ.get("TOKEN")

    parser = ArgumentParser(description="Plot a candlestick chart using the Tiingo API")
    parser.add_argument("symbol", help="Tiingo symbol")
    parser.add_argument("--from",
                        metavar="YYYY-MM-DD",
                        type=dt.date.fromisoformat,
                        default=dt.date.today() - dt.timedelta(days=365),
                        dest="date_from",
                        help="from date in ISO format")
    parser.add_argument("--to",
                        metavar="YYYY-MM-DD",
                        type=dt.date.fromisoformat,
                        dest="date_to",
                        help="to date in ISO format")
    parser.add_argument("--mav",
                        type=int,
                        nargs="+",
                        help="moving average windows")
    parser.add_argument("--volume",
                        action="store_true",
                        default=False,
                        help="add a volume plot")

    args = vars(parser.parse_args())
    args["token"] = token
    main(**args)
