"""Common messages used by multiple commands."""

from bonemeal.cli.components.message import info_message
from bonemeal.cli.components.utils import LineMode


def welcome_message() -> None:
    """Send a welcome message."""
    info_message(
        title="Welcome to Bone Meal!",
        description="The Minecraft pack management CLI.",
        icon="🦴",
        line_mode=LineMode.CLOSED_START,
    )
