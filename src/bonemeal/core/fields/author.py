"""Utilities related to the author field."""

import subprocess

from bonemeal.core.errors.main import BoneMealError
from bonemeal.core.utils.commands import check


class GitExecutionError(BoneMealError):
    """Error raised when the `git`-command raises an error."""

    title = "Git raised an error!"


def get_git_username() -> str | None:
    """Try to find the user's Git username or return None."""
    try:
        return check(["git", "config", "user.name"]).strip()
    except FileNotFoundError:
        return None
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
        raise GitExecutionError from err
