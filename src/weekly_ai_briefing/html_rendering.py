"""Renders the Jinja templates in html_templates/."""

import jinja2

from weekly_ai_briefing.config import TEMPLATE_FOLDER

# autoescape=True explicitly: select_autoescape would not match the ".html.j2" suffix.
ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_FOLDER),
    autoescape=True,
    undefined=jinja2.StrictUndefined,
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_template(name: str, **context: object) -> str:
    return ENVIRONMENT.get_template(name).render(**context)
