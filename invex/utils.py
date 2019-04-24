from functools import lru_cache
from datetime import datetime
import logging


from iexfinance import get_historical_data

import pandas as pd

log = logging.getLogger(__name__)


@lru_cache(maxsize=1024)
def fetch_benchmark_returns(start_date: datetime,
                            end_date: datetime) -> pd.DataFrame:
    benchmark = 'SPY'
    benchmark_price = \
        get_historical_data(benchmark, start=start_date, end=end_date,
                            output_format='pandas')['close']
    benchmark_price.index = pd.to_datetime(benchmark_price.index, utc=True)
    benchmark_price.name = benchmark

    benchmark_rets = benchmark_price.pct_change(1)
    return benchmark_rets
