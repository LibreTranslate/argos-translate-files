import abc
import os.path

from argostranslate.translate import ITranslation


class AbstractFile():
    supported_file_extensions = []

    def support(self, file_path: str):
        file_ext = os.path.splitext(file_path)[1]

        return file_ext in self.supported_file_extensions

    def get_output_path(self, underlying_translation: ITranslation, file_path: str):
        dir_path = os.path.dirname(file_path)
        file_name, file_ext = os.path.splitext(os.path.basename(file_path))
        to_code = underlying_translation.to_lang.code

        return dir_path + "/" + file_name + '_' + to_code + file_ext

    @abc.abstractmethod
    def translate(self, underlying_translation: ITranslation, file_path: str): raise NotImplementedError
