import argostranslate.argospm
from argostranslate import package


def test_boot_argos():
    """Test Argos translate models initialization"""
    argostranslate.argospm.install_package({"name": "translate-en_fr"})

    assert len(package.get_installed_packages()) == 1
