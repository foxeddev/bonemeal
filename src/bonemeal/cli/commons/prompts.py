"""Common prompts used by multiple commands."""

import enum
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from send2trash import send2trash

from bonemeal.cli.components.message import warning_message
from bonemeal.cli.components.prompt import Choice, single_option_prompt, text_prompt
from bonemeal.cli.utils.errors import UserCancelledError
from bonemeal.core.fields.author import get_git_username
from bonemeal.core.fields.mc_version import (
    MCVersion,
    find_mc_version,
    get_latest_mc_release,
)

if TYPE_CHECKING:
    from bonemeal.core.fields.mc_version import MCVersion


class PromptMode(enum.Enum):
    """Whether to show prompts to the user or always use default values."""

    SHOW_PROMPTS = enum.auto()
    USE_DEFAULT = enum.auto()


def path_prompt(
    path_str: str | None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
) -> Path:
    """Validate the path or show a prompt if none is specified."""
    if not path_str and prompt_mode is PromptMode.SHOW_PROMPTS:
        path_str = text_prompt(
            title="Where do you want to create your project?",
            description="Press enter to use the current directory.",
        )

    path = Path(path_str) if path_str else Path.cwd()

    if path.is_dir(follow_symlinks=False):
        # path is a directory

        if any(path.iterdir()):
            # path contains files

            warning_message("The specified directory is not empty!")
        else:
            return path

    elif path.exists():
        # path exists, but is not a directory

        warning_message("A file with the specified name already exists!")
    else:
        # path doesn't exist

        path.mkdir(parents=True)
        return path

    if not single_option_prompt(
        title="Do you want to overwrite it?",
        options=[
            Choice(value=True, title="OK"),
            Choice(value=False, title="Cancel"),
        ],
        default_option=1,
    ):
        # user declines to overwrite

        raise UserCancelledError

    # user accepts to overwrite

    send2trash(path)
    if path.is_dir():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    return path


def description_prompt(
    description: str | None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
) -> str:
    """Return the description or show a prompt if none is specified."""
    if not description and prompt_mode is PromptMode.SHOW_PROMPTS:
        description = text_prompt(
            title="What description do you want to add to your project?",
            description="Press enter to skip.",
        )

    return description or ""


def author_prompt(
    author: str | None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
) -> str:
    """Return the author or show a prompt if none is specified."""
    author = get_git_username() or author

    if not author and prompt_mode is PromptMode.SHOW_PROMPTS:
        author = text_prompt(
            title="What author do you want to set to your project?",
            description="Press enter to skip.",
        )

    return author or ""


def mc_version_prompt(
    mc_version_str: str | None,
    prompt_mode: PromptMode = PromptMode.SHOW_PROMPTS,
) -> MCVersion:
    """Validate the Minecraft version or show a prompt if none is specified."""
    if not mc_version_str and prompt_mode is PromptMode.SHOW_PROMPTS:
        mc_version_str = text_prompt(
            title="What Minecraft version do you want to use?",
            description="Press enter to use the latest release.",
        )

    return (
        find_mc_version(mc_version_str) if mc_version_str else get_latest_mc_release()
    )
