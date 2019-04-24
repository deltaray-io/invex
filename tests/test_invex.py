#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `invex` package."""
import os
import py

from click.testing import CliRunner
import pytest
from flexfolio.utils import run

from invex import cli


from .reports import ALL_FLEX_REPORTS


@pytest.mark.parametrize("flex_report", ALL_FLEX_REPORTS)  # type: ignore
def test_to_pdf_command(flex_report: str,
                        tmpdir: py.path.local  # pylint: disable=no-member
                        ) -> None:
    # Given the invex app with an input flex report and desired output pdf
    runner = CliRunner()
    output_filename = os.path.basename(flex_report).replace('xml', 'pdf')
    output_pdf = \
        '{tmpdir}/{filename}'.format(tmpdir=tmpdir, filename=output_filename)

    # When we call the to_pdf command
    result = runner.invoke(
        cli.main,
        ['to_pdf',
         flex_report,
         '--pdf-result-path', output_pdf])

    # Then it should create pdf file
    assert result.exit_code == 0
    file_type_result = run('file -b {output_pdf}'.format(
        output_pdf=output_pdf))
    assert file_type_result.output.startswith('PDF document')
