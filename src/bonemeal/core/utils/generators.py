"""Utitities for the project generators."""

import datetime


def id_to_name(project_id: str) -> str:
    """Convert a project ID to a properly formatted name."""
    return project_id.replace("-", " ").replace("_", " ").strip().capitalize()


def generate_mit_license(copyright_holder: str, year: int | None = None) -> str:
    """Generate an MIT license for the specified copyright holder."""
    year = year or datetime.datetime.now(tz=datetime.UTC).date().year
    return f"""MIT License

Copyright (c) {year} {copyright_holder}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def generate_readme(title: str, description: str | None = None) -> str:
    """Generate a README file."""
    return f"# {title}{f'\n\n{description}' if description else ''}\n"
