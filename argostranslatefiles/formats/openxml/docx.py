import zipfile

from argostranslate.tags import translate_tags
from argostranslate.translate import ITranslation
from bs4 import BeautifulSoup

from argostranslatefiles.formats.abstract_xml import AbstractXml


class Docx(AbstractXml):
    supported_file_extensions = ['.docx']

    def translate(self, underlying_translation: ITranslation, file_path: str):
        outzip_path = self.get_output_path(underlying_translation, file_path)

        inzip = zipfile.ZipFile(file_path, "r")
        outzip = zipfile.ZipFile(outzip_path, "w")

        for inzipinfo in inzip.infolist():
            with inzip.open(inzipinfo) as infile:
                if inzipinfo.filename == "word/document.xml":
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

    def get_texts(self, file_path: str):
        inzip = zipfile.ZipFile(file_path, "r")

        texts = ""

        for inzipinfo in inzip.infolist():
            if len(texts) > 4096:
                break
            with inzip.open(inzipinfo) as infile:
                if inzipinfo.filename == "word/document.xml":
                    soup = BeautifulSoup(infile.read(), 'xml')
                    texts += self.itag_of_soup(soup).text()

        inzip.close()

        return texts
