import re
import zipfile

import translatehtml
from argostranslate.tags import translate_tags
from argostranslate.translate import ITranslation
from bs4 import BeautifulSoup

from argostranslatefiles.formats.abstract_xml import AbstractXml


class Epub(AbstractXml):
    supported_file_extensions = ['.epub']

    def is_translatable(self, soup):
        return soup.text != ""

    def translate(self, underlying_translation: ITranslation, file_path: str):
        outzip_path = self.get_output_path(underlying_translation, file_path)

        inzip = zipfile.ZipFile(file_path, "r")
        outzip = zipfile.ZipFile(outzip_path, "w")


        for inzipinfo in inzip.infolist():
            with inzip.open(inzipinfo) as infile:
                if inzipinfo.filename == "OPS/content.opf" or inzipinfo.filename == "OPS/toc.ncx":
                    soup = BeautifulSoup(infile.read(), 'xml')

                    itag = self.itag_of_soup(soup)
                    translated_tag = translate_tags(underlying_translation, itag)
                    translated_soup = self.soup_of_itag(translated_tag)

                    outzip.writestr(inzipinfo.filename, str(translated_soup))
                elif re.search(r'OPS\/[a-zA-Z0-9\_]*.xhtml', inzipinfo.filename):
                    head = '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>'
                    content = str(infile.read(), 'utf-8')
                    head_present = content.startswith(head)

                    if head_present:
                        content = content[len(head):]

                    translated = str(translatehtml.translate_html(underlying_translation, content))

                    if head_present:
                        translated = str(head) + translated

                    outzip.writestr(inzipinfo.filename, translated)
                else:
                    outzip.writestr(inzipinfo.filename, infile.read())

        inzip.close()
        outzip.close()

        return outzip_path
