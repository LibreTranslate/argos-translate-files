# Argos Translate Files

Translate files using [Argos Translate](https://github.com/argosopentech/argos-translate).

## Supported file format

.txt, .odt, .odp, .docx, .pptx, .epub, .html

## Install

```
pip install argos-translate-files
```


## Example

```python
import os.path

import argostranslate.package, argostranslate.translate


import argostranslatefiles
from argostranslatefiles import argostranslatefiles

from_code = "fr"
to_code = "en"

installed_languages = argostranslate.translate.get_installed_languages()
from_lang = list(filter(
    lambda x: x.code == from_code,
    installed_languages))[0]
to_lang = list(filter(
    lambda x: x.code == to_code,
    installed_languages))[0]
underlying_translation = from_lang.get_translation(to_lang)

argostranslatefiles.translate_file(underlying_translation, os.path.abspath('path/to/file.txt'))

```
