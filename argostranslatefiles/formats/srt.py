import pysrt
from argostranslate.translate import ITranslation
from argostranslatefiles.abstract_file import AbstractFile


class Srt(AbstractFile):
    supported_file_extensions = ['.srt']

    def translate(self, underlying_translation: ITranslation, file_path: str):
        outfile_path = self.get_output_path(underlying_translation, file_path)

        subs = pysrt.open(file_path)

        for sub in subs:
            sub.text = underlying_translation.translate(sub.text)

        subs.save(outfile_path, encoding='utf-8')

        return outfile_path


    def get_texts(self, file_path: str):
        subs = pysrt.open(file_path)
        text = "\n".join([sub.text for sub in subs])
        return text[0:4096]
