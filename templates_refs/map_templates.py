""" Function for mapping a template folder and creating references. """

from flask import Flask
from pathlib import Path

from .errors import FolderNotFoundError, NoTemplatesError


def map_templates(app: Flask) -> dict[str, Path] | FolderNotFoundError | NoTemplatesError:
    """ Walks through app.template_folder and creates a dict of shortened template names matching their "full name" as recognized by Jinja, which is a string representation of their path relative to the template folder.
    In case of similarly named templates, appends the name of the first parent directory to the begining of the shortened template name for disambiguation.
    If no template_folder has been set, defaults to 'templates' folder in app root directory if that folder exists. """

    references = {}

    tf_path = Path(app.template_folder) if app.template_folder is not None else Path(
        app.instance_path).parent / "templates"

    bp_paths = [Path(bp.template_folder)
                for bp in list(app.blueprints.values()) if bp.template_folder is not None]

    if tf_path.exists():
        references = map_dir(tf_path)

        for path in bp_paths:
            references.update(map_dir(path))
        if len(references.items()) > 0:
            return references

        return NoTemplatesError(template_folder=tf_path)
    return FolderNotFoundError(template_folder=tf_path)


def map_dir(dir_path: Path):
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
