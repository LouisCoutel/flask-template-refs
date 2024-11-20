""" Flask extension for creating template references from a multi-level template folder
and making them available in templates themselves through globals """


from os import PathLike
from flask import Flask
from pathlib import Path
from flask.sansio.blueprints import Blueprint

from . import references
from .errors import FolderNotFoundError


def map_dir(refs: dict, dir_path: Path, blueprint_name: str | None = None) -> dict:
    """ Walks through the provided directory
    and creates a dict of shortened template names
    matching their "full name" as recognized by Jinja,
    which is a string representation of their path relative to the template folder.

    In case of similarly named templates,
    appends the name of the first parent directory to the begining
    of the shortened template name for disambiguation. """

    for dir in dir_path.walk(top_down=True):
        root = dir[0]
        files = dir[2]

        for file in files:
            name = file.split(".")[0]
            path = (root / file).relative_to(dir_path).__str__()

            if blueprint_name:
                name = blueprint_name + "_" + name

            if not refs.get(name):
                refs[name] = path

            else:
                refs[root.name + "_" + name] = path

    return refs


def resolve_tf(app_root_path: Path,
               template_folder: str | PathLike | Path) -> Path:
    """ Creates a Path object for the app template_folder, then verifies that it exists.
    This allows the extension to work with pathlib all the way through. """

    template_folder = app_root_path / \
        template_folder if isinstance(
            template_folder, str | PathLike) else template_folder

    if template_folder.exists():
        return template_folder

    raise FolderNotFoundError(template_folder)


class FlaskTemplateRefs():
    """ Manages creating templates references,
    writing to reference stub file to enable auto-completion and
    initializing the app. """

    _refs_file = Path(__file__).parent / "references.pyi"

    @classmethod
    def reset_refs_file(cls) -> None:
        """ Resets reference stub file for testing purposes """

        lines = ["class TemplateRefs():", "    pass", "refs = TemplateRefs()"]

        cls._refs_file.write_text(str.join("\n", lines))

    def __init__(self, app: Flask) -> None:
        self.refs = {}
        self.project_root_path = Path(app.instance_path).parent
        self.app_root_path = self.project_root_path / app.name

        app.template_folder = (
            app.template_folder if app.template_folder is not None else "templates")

        self.app_tf_path = resolve_tf(
            self.app_root_path, app.template_folder)

        self.refs = map_dir(self.refs, self.app_tf_path)

        for bp in app.iter_blueprints():
            self._map_blueprint(bp)

        if self.refs:
            self._write_refs()
            self._create_attributes()

        self._init_app(app)

    def _map_blueprint(self, blueprint: Blueprint) -> dict:
        """ Updates self.refs dict with templates for a specific blueprint
        provided they are not already included in the main app template folder. """

        bp_root_path = self.project_root_path / blueprint.root_path

        if blueprint.template_folder is not None:
            bp_tf_path = resolve_tf(bp_root_path, blueprint.template_folder)

            if self.app_tf_path not in bp_tf_path.parents:
                bp_refs = map_dir(self.refs, bp_tf_path, blueprint.name)

                if bp_refs:
                    self.refs.update(bp_refs)

        return self.refs

    def _write_refs(self) -> None:
        """ Updates TemplateRefs stub file with template references as attributes,
        which enables auto-completion. """

        lines = ["class TemplateRefs():"]

        for key in list(self.refs.keys()):
            lines.append(f"    {key}: str")

        lines.append("refs: TemplateRefs")

        self._refs_file.write_text(str.join("\n", lines))

    def _create_attributes(self) -> references.TemplateRefs:
        """ Sets references as attributes of the TemplateRefs instance,
        matching those defined in the class stub file. """

        refs = references.refs

        for key, value in self.refs.items():
            refs.__setattr__(key, value)

        return references.refs

    def _init_app(self, app: Flask) -> None:
        """ Sets the self.refs dict as a Jinja global accessible in templates """

        for key, value in self.refs.items():
            app.jinja_env.globals[key.upper()] = value
