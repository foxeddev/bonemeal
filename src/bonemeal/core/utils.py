"""Utilities."""

import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def run_silent(cmd: list[str | Path]) -> subprocess.CompletedProcess[bytes]:
    """Run a command using subprocess without showing the output to the user.

    Raises `subprocess.CalledProcessError` when the command fails to execute.

    Raises `subprocess.TimeoutExpired` when the command doesn't respond within 20
    seconds.
    """
    return subprocess.run(
        args=cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
        timeout=20,
    )


def check_silent(cmd: list[str | Path]) -> str:
    """Run a command without showing the output to the user and returns the result.

    Raises `subprocess.CalledProcessError` when the command fails to execute.

    Raises `subprocess.TimeoutExpired` when the command doesn't respond within 20
    seconds.
    """
    return subprocess.check_output(
        args=cmd,
        stderr=subprocess.DEVNULL,
        timeout=20,
        text=True,
    )
