""" Custom exceptions """

from pathlib import Path


class FolderNotFoundError(Exception):
    """ The specified template folder does not exists. """

    def __init__(self, template_folder: Path | None):
        self.add_note(
            f"Template folder '{template_folder}' does not exists.")
