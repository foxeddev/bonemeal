"""Common messages used by multiple commands."""

from packseed.cli.components.message import success_message
from packseed.cli.components.utils import LineMode


def welcome_message() -> None:
    """Send a welcome message."""
    success_message(
        title="Welcome to PackSeed!",
        description="The Minecraft pack manager.",
        line_mode=LineMode.CLOSED_START,
    )
