from typing import NamedTuple, Text

import frontmatter

from .constants import MAX_FILE_SIZE
from .errors import DevCliError


class DevKey(NamedTuple):
    """
    That's a (approximate) key that allows to spot an article that already
    exists in the API.
    """

    name: Text
    value: Text


class DevParser:
    """
    Parses a dev.to article Markdown, especially to extract the front matter.
    """

    def __init__(self, file_path: Text) -> None:
        self.file_path = file_path

        try:
            with open(file_path, encoding="utf-8") as f:
                self.file_content = f.read(MAX_FILE_SIZE)

                if f.read(1):
                    raise DevCliError(f'File "{file_path}" is too big')
        except IOError as e:
            raise DevCliError(f'Could not open "{file_path}": {e}')

        self.front_matter, self.markdown = frontmatter.parse(self.file_content)

    def get_key(self, key_name: Text) -> DevKey:
        """
        Extracts the DevKey object from the parsed article based on the key
        name, provided that the key exists.
        """

        if key_name not in self.front_matter:
            raise DevCliError(
                f'Cannot find publishing key "{key_name}" in file\'s front matter'
            )

        return DevKey(key_name, self.front_matter[key_name])
