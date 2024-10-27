import translatehtml
from argostranslate.translate import ITranslation

from argostranslatefiles.abstract_file import AbstractFile
from bs4 import BeautifulSoup


class Html(AbstractFile):
    supported_file_extensions = ['.html']

    def translate(self, underlying_translation: ITranslation, file_path: str):
        outfile_path = self.get_output_path(underlying_translation, file_path)

        infile = open(file_path, "r")
        outfile = open(outfile_path, "w")

        content = infile.read()

        head = '<!DOCTYPE html>'
        head_present = content.startswith(head)

        if head_present:
            content = content[len(head):]

        translated = str(translatehtml.translate_html(underlying_translation, content))

        if head_present:
            translated = str(head) + translated

        outfile.write(translated)

        infile.close()
        outfile.close()

        return outfile_path

    def get_texts(self, file_path: str):
        infile = open(file_path, "r")

        content = infile.read()

        soup = BeautifulSoup(content, "html.parser")
        return translatehtml.itag_of_soup(soup).text()[0:4096]
