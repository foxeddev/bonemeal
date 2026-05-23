"""Common messages used by multiple commands."""

from bonemeal.cli.components.message import success_message
from bonemeal.cli.components.utils import LineMode


def welcome_message() -> None:
    """Send a welcome message."""
    success_message(
        title="Welcome to Bonemeal!",
        description="The Minecraft pack manager.",
        icon="🦴",
        line_mode=LineMode.CLOSED_START,
    )
