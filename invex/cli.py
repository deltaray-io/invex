# -*- coding: utf-8 -*-

"""Console script for invex."""
import sys
import logging
from typing import Optional

import click

from flexfolio.flex_statement import FlexStatement, ALL_MODELS
from flexfolio.cli import fetch_statement_logic
from invex.pyfolio_wrapper import create_pdf_report
from invex.utils import fetch_benchmark_returns


log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@click.group()
def main() -> None:
    pass


@main.command()
@click.argument(
    'ib-api-token',
    nargs=1,
    type=click.STRING
)
@click.argument(
    'ib-query-id',
    nargs=1,
    type=click.STRING
)
@click.argument(
    'target-file',
    nargs=1,
    type=click.Path(exists=False, writable=True,
                    file_okay=True, dir_okay=False)
)
def fetch_statement(ib_api_token: str, ib_query_id: str,
                    target_file: str) -> None:
    return fetch_statement_logic(ib_api_token, ib_query_id, target_file)


@main.command()
@click.argument(
    'flex-report-path',
    nargs=1,
    type=click.Path(exists=True)
)
@click.option(
    '--model',
    default=ALL_MODELS
)
@click.option(
    '--pdf-result-path',
    default=None
)
def to_pdf(flex_report_path: str,
           pdf_result_path: Optional[str],
           model: str) -> int:
    statement = FlexStatement(flex_report_path)

    benchmark_rets = fetch_benchmark_returns(
        start_date=statement.returns(model).index[0],
        end_date=statement.returns(model).index[-1])

    if not pdf_result_path:
        pdf_result_path = flex_report_path.replace('.xml', '.pdf')
    create_pdf_report(pdf_result_path,
                      statement.returns(model),
                      statement.positions(model),
                      statement.transactions(model),
                      benchmark_rets)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
