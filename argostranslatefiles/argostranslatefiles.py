from argostranslate.translate import ITranslation

from argostranslatefiles.formats.html import Html
from argostranslatefiles.formats.opendocument.odp import Odp
from argostranslatefiles.formats.opendocument.odt import Odt
from argostranslatefiles.formats.openxml.docx import Docx
from argostranslatefiles.formats.openxml.pptx import Pptx
from argostranslatefiles.formats.txt import Txt
from argostranslatefiles.formats.epub import Epub
from argostranslatefiles.formats.srt import Srt
from argostranslatefiles.formats.pdf import Pdf

def get_supported_formats():
    return [
        Txt(),
        Odt(),
        Odp(),
        Docx(),
        Pptx(),
        Epub(),
        Html(),
        Srt(),
        Pdf(),
    ]


def translate_file(underlying_translation: ITranslation, file_path: str):
    """Translate a file.

    Args:
        underlying_translation (argostranslate.translate.ITranslation): Argos Translate Translation
        file_path (str): file path

    Returns:
        file_path: Translated file
    """

    for supported_format in get_supported_formats():
        if supported_format.support(file_path):
            return supported_format.translate(underlying_translation, file_path)

    return False


def get_texts(file_path: str):
    """Get the file contents.

    Args:
        file_path (str): file path

    Returns:
        texts: File contents
    """

    for supported_format in get_supported_formats():
        if supported_format.support(file_path):
            return supported_format.get_texts(file_path)

    return False
