"""Utilities for running commands."""

import subprocess

TIMEOUT = 20


def run(
    cmd: list[str],
    timeout: int = TIMEOUT,
) -> None:
    """Run a command.

    Raises `subprocess.CalledProcessError` when the command fails to execute.

    Raises `subprocess.TimeoutExpired` when the command doesn't respond within 20
    seconds.
    """
    subprocess.run(
        args=cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
        timeout=timeout,
    )


def check(
    cmd: list[str],
    timeout: int = TIMEOUT,
) -> str:
    """Run a command and return the result.

    Raises `subprocess.CalledProcessError` when the command fails to execute.

    Raises `subprocess.TimeoutExpired` when the command doesn't respond within 20
    seconds.
    """
    return subprocess.check_output(
        args=cmd,
        stderr=subprocess.DEVNULL,
        timeout=timeout,
        text=True,
    )
