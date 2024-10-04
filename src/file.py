from os.path import join


class FileManager:
    """
    Class for handling localization (and maybe other file IO in future).
    Stores localization in dictionary.
    """

    ASSETS_DIR = 'assets'

    @staticmethod
    def write_file(name: str, content: str, append: bool = False, assets: bool = False):
        """
        Save output file.

        :param name: File name.
        :param content: File content (utf-8 string).
        :param append: True for appending to file, false for rewriting.
        :param assets: True for saving to 'assets' directory, false otherwise.
        """
        name = join(FileManager.ASSETS_DIR, name) if assets else name
        with open(name, 'a' if append else 'w', encoding='utf-8') as file:
            file.write(content)
