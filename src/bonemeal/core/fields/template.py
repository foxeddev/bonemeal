"""Utilities related to the template field."""

from dataclasses import dataclass

from bonemeal.core.errors.main import BoneMealError


@dataclass(frozen=True, slots=True)
class Template:
    """Class representing a project template."""

    title: str
    includes: list[str]
    description: str | None = None


class TemplateNotFoundError(BoneMealError):
    """Error raised when the queried template could not be found."""

    def __init__(self, query: str | None = None) -> None:
        """Initialize an error from an optional query string."""
        self.title = f'"{query}" is not a valid template!'


def find_template(query: str, templates: dict[str, Template]) -> Template:
    """Return the first template whose title matches the query."""
    try:
        return next(
            template
            for template in templates.values()
            if template.title.lower() == query.lower()
        )

    except StopIteration as err:
        raise TemplateNotFoundError(query) from err
