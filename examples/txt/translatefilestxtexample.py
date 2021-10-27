import os.path

from argostranslate import translate

from argostranslatefiles import argostranslatefiles

installed_languages = translate.get_installed_languages()
underlying_translation = installed_languages[0].get_translation(installed_languages[1])
argostranslatefiles.translate_file(underlying_translation, os.path.abspath('examples/txt/example.txt'))
