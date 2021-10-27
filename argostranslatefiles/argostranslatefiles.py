from argostranslate.translate import ITranslation

from argostranslatefiles.formats.opendocument.odt import Odt
from argostranslatefiles.formats.openxml.docx import Docx
from argostranslatefiles.formats.openxml.pptx import Pptx
from argostranslatefiles.formats.txt import Txt


def get_supported_formats():
    return [
        Txt(),
        Odt(),
        Docx(),
        Pptx()
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
