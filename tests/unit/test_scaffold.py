"""Smoke checks for the initial architecture scaffold."""

from microcode import __version__
from microcode.cli.commands import SlashCommand, parse_slash_command


def test_version_is_mvp() -> None:
    assert __version__ == "0.1.0"


def test_slash_command_parser() -> None:
    assert parse_slash_command('/why "src/example.py"') == SlashCommand(
        name="why",
        args=("src/example.py",),
    )


def test_plain_text_is_not_a_command() -> None:
    assert parse_slash_command("explain this project") is None
