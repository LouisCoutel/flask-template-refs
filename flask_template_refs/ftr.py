""" Flask extension for creating template references from a multi-level template folder and making them available in templates themselves through globals """

from os import PathLike
from flask import Flask
from pathlib import Path

from .errors import FolderNotFoundError

from . import references


def map_dir(dir_path: Path) -> dict:
    """ Walks through the provided directory and creates a dict of shortened template names matching their "full name" as recognized by Jinja,
    which is a string representation of their path relative to the template folder.

    In case of similarly named templates, appends the name of the first parent directory to the begining of the shortened template name for disambiguation. """

    references = {}

    for dir in dir_path.walk():
        root = dir[0]
        files = dir[2]

        for file in files:
            name = file.split(".")[0]
            path = (root / file).relative_to(dir_path).__str__()

            if not references.get(name):
                references[name] = path

            else:
                references[root.name + "_" + name] = path

    return references


def resolve_tf(app_root_path: Path, template_folder: str | PathLike | Path) -> Path:
    """ Creates a Path object for the app template_folder, then verifies that it exists.
    This allows the extension to work with pathlib all the way through. """

    template_folder = app_root_path / \
        template_folder if isinstance(
            template_folder, str | PathLike) else template_folder

    if template_folder.exists():
        return template_folder

    raise FolderNotFoundError(template_folder)


class FlaskTemplateRefs():
    """ Manages creating templates references, writing to reference stub file to enable auto-completion and initializing the app. """

    _refs_file = Path(__file__).parent / "references.pyi"
    refs: dict

    @classmethod
    def reset_refs_file(cls) -> None:
        """ Resets reference stub file for testing purposes """

        lines = ["class TemplateRefs():", "    pass", "refs = TemplateRefs()"]

        cls._refs_file.write_text(str.join("\n", lines))

    def __init__(self, app: Flask) -> None:
        app_root_path = Path(app.instance_path).parent / app.name
        template_folder_path = resolve_tf(
            app_root_path, app.template_folder)

        self.refs = map_dir(template_folder_path)

        bp_template_folders = [bp.template_folder for bp in app.iter_blueprints(
        ) if (bp.template_folder is not None and bp.template_folder != app.template_folder)]

        self._map_blueprints_tfs(template_folder_path,
                                 bp_template_folders, app_root_path)

        if self.refs:
            self._write_refs()
            self._create_attributes()

        self._init_app(app)

    def _map_blueprints_tfs(self,
                            template_folder_path: Path,
                            bp_template_folders: list[str | PathLike[str]],
                            app_root_path: Path) -> None:
        """ Updates self.refs dict with templates from blueprint folders that are not included in the main app template folder. """

        for bp_tf in bp_template_folders:
            bp_tf_path = resolve_tf(app_root_path, bp_tf)

            if template_folder_path not in bp_tf_path.parents:
                bp_refs = map_dir(bp_tf_path)

                self.refs.update(bp_refs)

    def _write_refs(self) -> None:
        """ Updates TemplateRefs stub file with template references as attributes, which enables auto-completion. """

        lines = ["class TemplateRefs():"]

        for key in list(self.refs.keys()):
            lines.append(f"    {key}: str")

        lines.append("refs: TemplateRefs")

        self._refs_file.write_text(str.join("\n", lines))

    def _create_attributes(self) -> None:
        """ Sets references as attributes of the TemplateRefs instance, matching those defined in the class stub file. """

        refs = references.refs

        for key, value in self.refs.items():
            refs.__setattr__(key, value)

    def _init_app(self, app: Flask) -> None:
        """ Sets the self.refs dict as a Jinja global accessible in templates """

        for key, value in self.refs.items():
            app.jinja_env.globals[key] = value
