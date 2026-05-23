"""Utilities."""

import subprocess


def get_git_username() -> str | None:
    """Try to find the user's Git username or return None."""
    try:
        return subprocess.check_output(
            # this is fine because no sensitive data is passed
            ["git", "config", "user.name"],  # noqa: S607
            text=True,
        ).strip()

    except subprocess.CalledProcessError:
        return None
