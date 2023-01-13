from typing import Sequence, Union

import click
from click.testing import CliRunner, Result
from stactools.testing.test_data import TestData

from stactools.sentinel1.commands import create_sentinel1_command

test_data = TestData(__file__)


@click.group()
def test_cli() -> None:
    pass


create_sentinel1_command(test_cli)


def run_command(command: Union[str, Sequence[str]]) -> Result:
    runner = CliRunner()
    result = runner.invoke(test_cli, command, catch_exceptions=False)
    if result.output:
        print(result.output)
    return result
