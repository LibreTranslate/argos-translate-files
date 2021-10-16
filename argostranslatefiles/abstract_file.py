import abc
import os.path


class AbstractFile():
    supported_file_extensions = []

    def support(self, file_path: str):
        file_ext = os.path.splitext(file_path)[1]

        return file_ext in self.supported_file_extensions

    @abc.abstractmethod
    def translate(self, underlying_translation, file_path): raise NotImplementedError
