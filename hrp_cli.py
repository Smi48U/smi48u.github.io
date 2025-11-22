"""Terminal HRP allocator using ticker list from a text file.

Usage example:
    python hrp_cli.py --tickers-file tickers_example.txt --start 2018-01-01

The script downloads price data from Yahoo Finance and prints Hierarchical Risk
Parity weights for the provided symbols.
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import yfinance as yf
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute HRP allocation weights from Yahoo Finance prices.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--tickers-file",
        required=True,
        type=Path,
        help="Text file containing one ticker per line; blank lines and lines starting with # are ignored.",
    )
    parser.add_argument(
        "--start",
        default="2018-01-01",
        help="Start date for historical data (YYYY-MM-DD).",
    )
    parser.add_argument(
        "--end",
        default=None,
        help="Optional end date for historical data (YYYY-MM-DD). If omitted, uses the latest available data.",
    )
    parser.add_argument(
        "--method",
        default="ward",
        choices=["ward", "single", "average", "complete"],
        help="Linkage method for hierarchical clustering.",
    )
    return parser.parse_args()


def read_tickers(path: Path) -> List[str]:
    if not path.exists():
        raise FileNotFoundError(f"Ticker file not found: {path}")

    tickers = []
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        tickers.append(stripped)

    if len(tickers) < 2:
        raise ValueError("Provide at least two tickers in the ticker file.")
    return tickers


def fetch_prices(tickers: List[str], start: str, end: str | None) -> pd.DataFrame:
    prices = (
        yf.download(tickers, start=start, end=end, progress=False)["Adj Close"]
        .dropna(how="all")
    )
    if prices.empty:
        raise ValueError("No price data returned; check tickers and date range.")
    return prices


def compute_hrp_weights(prices: pd.DataFrame, method: str = "ward") -> pd.Series:
    returns = np.log(prices / prices.shift(1)).dropna()
    if returns.empty or returns.shape[1] < 2:
        raise ValueError("Not enough return data to compute covariance.")

    corr = returns.corr()
    dist = np.sqrt(0.5 * (1 - corr))

    condensed_dist = squareform(dist.values, checks=False)
    link = linkage(condensed_dist, method=method)

    sorted_idx = _get_quasi_diag(link)
    ordered_tickers = corr.index[sorted_idx]

    cov = returns.cov()
    weights = _hrp_allocation(cov, ordered_tickers)
    return weights.sort_values(ascending=False)


def _get_quasi_diag(link: np.ndarray) -> List[int]:
    sort_ix = pd.Series([link[-1, 0], link[-1, 1]])
    num_items = link.shape[0] + 1
    while sort_ix.max() >= num_items:
        sort_ix.index = range(0, sort_ix.shape[0] * 2, 2)
        df0 = sort_ix[sort_ix >= num_items]
        i = df0.index
        j = df0.values - num_items
        sort_ix[i] = link[j, 0]
        df0 = pd.Series(link[j, 1], index=i + 1)
        sort_ix = pd.concat([sort_ix, df0])
        sort_ix = sort_ix.sort_index()
    return sort_ix.astype(int).tolist()


def _cluster_variance(cov: pd.DataFrame, cluster_items: List[str]) -> float:
    cov_slice = cov.loc[cluster_items, cluster_items]
    w = np.ones(len(cluster_items)) / len(cluster_items)
    return float(np.dot(w, np.dot(cov_slice, w)))


def _hrp_allocation(cov: pd.DataFrame, sorted_items: List[str]) -> pd.Series:
    weights = pd.Series(1.0, index=sorted_items)
    clusters = [sorted_items]

    while clusters:
        clusters = [c[len(c) // 2 :] for c in clusters if len(c) > 1] + [c[: len(c) // 2] for c in clusters if len(c) > 1]
        for i in range(0, len(clusters), 2):
            if i + 1 >= len(clusters):
                continue
            c1, c2 = clusters[i], clusters[i + 1]
            var1 = _cluster_variance(cov, c1)
            var2 = _cluster_variance(cov, c2)
            alpha = 1 - var1 / (var1 + var2)
            weights[c1] *= alpha
            weights[c2] *= 1 - alpha
    return weights / weights.sum()


def main() -> None:
    args = parse_args()
    tickers = read_tickers(args.tickers_file)

    try:
        start = dt.date.fromisoformat(args.start)
    except ValueError as exc:  # noqa: PERF203 - clarity
        raise SystemExit(f"Invalid start date: {args.start}") from exc

    end_date = None
    if args.end:
        try:
            end_date = dt.date.fromisoformat(args.end)
        except ValueError as exc:  # noqa: PERF203 - clarity
            raise SystemExit(f"Invalid end date: {args.end}") from exc

    prices = fetch_prices(tickers, start.isoformat(), end_date.isoformat() if end_date else None)
    weights = compute_hrp_weights(prices, method=args.method)

    print("\nHRP weights (descending):")
    for ticker, weight in weights.items():
        print(f"  {ticker}: {weight:.4f}")

    print("\nData window:")
    print(f"  Start: {prices.index.min().date()}")
    print(f"  End:   {prices.index.max().date()}")
    print(f"  Observations: {len(prices)}")


if __name__ == "__main__":
    main()
