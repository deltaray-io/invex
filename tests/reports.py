import os
from glob import glob
from typing import List, Optional

import pytest
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))


def flex_reports(x_fail_patterns: Optional[List[str]] = None) -> List[str]:
    all_reports = sorted(glob("%s/tests/statements/*/*.xml" % PROJECT_ROOT))
    marked_reports = []  # type: List[str]
    x_fail_patterns = x_fail_patterns or []

    for report in all_reports:
        if any(pattern in report for pattern in x_fail_patterns):
            report_to_add = pytest.param(report, marks=pytest.mark.xfail)
        else:
            report_to_add = report
        marked_reports.append(report_to_add)

    return marked_reports


ALL_FLEX_REPORTS = flex_reports()


def _expected_filename(flex_report_path: str, result_type: str) -> str:
    return \
        os.path.splitext(flex_report_path)[0] + '-exp-' + result_type + '.csv'


def load_expected_results(flex_report_path: str,
                          result_type: str) -> pd.DataFrame:
    df = pd.read_csv(
        _expected_filename(flex_report_path, result_type),
        parse_dates=True,
        header=[0, 1],
        index_col=0)
    if isinstance(df.index, pd.DatetimeIndex):
        df.index = df.index.tz_localize('UTC')
    return df


def store_expected_results(flex_report_path: str,
                           result_type: str,
                           df: pd.DataFrame) -> None:
    df.to_csv(_expected_filename(flex_report_path, result_type))
