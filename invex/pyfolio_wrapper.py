# pylint: disable=wrong-import-position, ungrouped-imports
from contextlib import contextmanager
import logging
from typing import Generator, Optional

import pandas as pd
import matplotlib

matplotlib.use('Agg')  # Need to set this before pyfolio import

import pyfolio  # noqa: E402
import matplotlib.pyplot  # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages  # noqa: E402


log = logging.getLogger(__name__)


@contextmanager
def capture_mpl_figures_to_pdf(filename: str) -> Generator:
    _orig_pyplot_show = matplotlib.pyplot.show

    with PdfPages(filename) as pdf:
        def save_to_pdf() -> None:
            pdf.savefig()

        matplotlib.pyplot.show = save_to_pdf

        yield

    matplotlib.pyplot.show = _orig_pyplot_show


# pylint: disable=unused-argument
def dataframe_to_mpl_plot(table: pd.DataFrame,
                          name: Optional[str] = None,
                          float_format: Optional[str] = None,
                          formatters: Optional[str] = None,
                          header_rows: Optional[str] = None) -> None:
    if isinstance(table, pd.Series):
        table = pd.DataFrame(table)

    if name is not None:
        table.columns.name = name

    fig = matplotlib.pyplot.figure(figsize=(20, 14))
    axes = fig.add_subplot(111, facecolor='white')
    axes.get_xaxis().set_visible(False)
    axes.get_yaxis().set_visible(False)
    table = axes.table(cellText=table.values,
                       colWidths=[0.1] * len(table.columns),
                       rowLabels=table.index,
                       colLabels=table.columns,
                       loc='center',
                       cellLoc='center',
                       rowLoc='center')
    table.scale(2, 2)
    matplotlib.pyplot.show()
    matplotlib.pyplot.close(fig)


@contextmanager
def pf_print_table_to_mpl() -> Generator:
    _orig_print_table = pyfolio.utils.print_table

    pyfolio.utils.print_table = dataframe_to_mpl_plot
    pyfolio.perf_attrib.print_table = dataframe_to_mpl_plot
    pyfolio.round_trips.print_table = dataframe_to_mpl_plot

    yield

    pyfolio.utils.print_table = _orig_print_table
    pyfolio.perf_attrib.print_table = _orig_print_table
    pyfolio.round_trips.print_table = _orig_print_table


def create_pdf_report(filename: str,
                      returns: pd.Series,
                      positions: pd.DataFrame,
                      transactions: pd.DataFrame,
                      benchmark_rets: pd.DataFrame) -> None:
    with capture_mpl_figures_to_pdf(filename):
        with pf_print_table_to_mpl():
            pyfolio.create_full_tear_sheet(
                returns, positions=positions, transactions=transactions,
                round_trips=True,
                benchmark_rets=benchmark_rets, bootstrap=None)

    log.info("Report created: {filename}".format(**locals()))
