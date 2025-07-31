import os.path
import argparse

from argostranslate import translate

from argostranslatefiles import argostranslatefiles

"""
# Usage

python3 examples/translatefilestxtexample.py examples/example.epub
python3 examples/translatefilestxtexample.py examples/example.txt
python3 examples/translatefilestxtexample.py examples/example.odt
python3 examples/translatefilestxtexample.py examples/example.html
python3 examples/translatefilestxtexample.py examples/example.srt
python3 examples/translatefilestxtexample.py examples/example.pdf
"""

# Parse command line args
parser = argparse.ArgumentParser(description='Translate a file.')
parser.add_argument('file_path', type=str, help='Path to file to translate')
args = parser.parse_args()

# Translate file
installed_languages = translate.get_installed_languages()
underlying_translation = installed_languages[0].get_translation(installed_languages[1])
print(argostranslatefiles.translate_file(underlying_translation, os.path.abspath(args.file_path)))
