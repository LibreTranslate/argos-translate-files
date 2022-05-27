from argostranslate.translate import ITranslation

from argostranslatefiles.abstract_file import AbstractFile


class Txt(AbstractFile):
    supported_file_extensions = ['.txt']

    def translate(self, underlying_translation: ITranslation, file_path: str):
        outfile_path = self.get_output_path(underlying_translation, file_path)

        infile = open(file_path, "r")
        outfile = open(outfile_path, "w")

        translated_text = underlying_translation.translate(infile.read())
        outfile.write(translated_text)

        infile.close()
        outfile.close()

        return outfile_path
