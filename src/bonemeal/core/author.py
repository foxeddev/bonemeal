"""Helper function related to the project author field."""

import subprocess

from bonemeal.core.utils import check_silent


def get_git_username() -> str | None:
    """Try to find the user's Git username or return None."""
    try:
        return check_silent(["git", "config", "user.name"]).strip()

    except subprocess.CalledProcessError, subprocess.TimeoutExpired:
        return None
