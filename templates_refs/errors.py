""" Custom exceptions """

from pathlib import Path


class NoTemplatesError(Exception):
    """ No template could be found in app template_folder.
        Is used as a return value rather than a classic exception. """

    def __init__(self, template_folder: Path):
        self.template_folder = template_folder.name
        self.add_note(
            f"No templates found in folder '{template_folder.name}'.")


class FolderNotFoundError(Exception):
    """ The specified template folder does not exists.
        Is used as a return value rather than a classic exception. """

    def __init__(self, template_folder: Path):
        self.template_folder = template_folder.name
        self.add_note(
            f"Template folder '{template_folder.name}' does not exists.")
