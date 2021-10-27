import zipfile

from argostranslate.tags import translate_tags
from argostranslate.translate import ITranslation
from bs4 import BeautifulSoup

from argostranslatefiles.formats.abstract_xml import AbstractXml


class Odt(AbstractXml):
    supported_file_extensions = ['.odt']

    def translate(self, underlying_translation: ITranslation, file_path: str):
        outzip_path = self.get_output_path(underlying_translation, file_path)

        inzip = zipfile.ZipFile(file_path, "r")
        outzip = zipfile.ZipFile(outzip_path, "w")

        for inzipinfo in inzip.infolist():
            with inzip.open(inzipinfo) as infile:
                if inzipinfo.filename == "content.xml":
                    soup = BeautifulSoup(infile.read(), 'xml')

                    itag = self.itag_of_soup(soup)
                    translated_tag = translate_tags(underlying_translation, itag)
                    translated_soup = self.soup_of_itag(translated_tag)

                    outzip.writestr(inzipinfo.filename, str(translated_soup))
                else:
                    outzip.writestr(inzipinfo.filename, infile.read())

        inzip.close()
        outzip.close()

        return outzip_path
