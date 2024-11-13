""" Flask extension for creating template references from a multi-level template folder and making them available in templates themselves through globals """

from flask import Flask
from pathlib import Path

from .errors import FolderNotFoundError, NoTemplatesError
from .map_templates import map_templates


class JinjaTemplatesRefs():
    """ Manages creating templates references, writing to reference file and initializing the app. """

    _refs_file = Path(__file__).parent / "references.py"
    refs: dict[str, Path] | NoTemplatesError | FolderNotFoundError

    def __init__(self, app: Flask):
        self._reset_refs()
        self.init_app(app)

    def _reset_refs(self) -> None:
        """ Over write reference file with empty class """

        lines = ['""" Class for storing template references pointing to their full name as recognized by Jinja """',
                 "from pathlib import Path", "class TemplateRefs():", '    """ Stores references """', "    pass", "refs = TemplateRefs()"]

        self._refs_file.write_text(str.join("\n", lines))

    def write_refs(self) -> None:
        """ Overwrite reference file with template references as attributes of class TemplateRefs """

        if not (isinstance(self.refs, NoTemplatesError) or isinstance(self.refs, FolderNotFoundError)):
            lines = ['""" Class for storing template references pointing to their full name as recognized by Jinja """',
                     "from pathlib import Path", "class TemplateRefs():", '    """ Stores references """']

            for key, value in self.refs.items():
                lines.append(f"    {key} = '{value}'")

            lines.append("refs = TemplateRefs()")

            self._refs_file.write_text(str.join("\n", lines))

    def init_app(self, app: Flask) -> None:
        """ Checks if any templates have been found, if so write template references to file and set them as a dict in Jinja globals """

        self.refs = map_templates(app)

        if not isinstance(self.refs, NoTemplatesError):
            self.write_refs()

            app.jinja_env.globals.update(template_refs=self.refs)
