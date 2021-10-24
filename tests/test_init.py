import argostranslatefiles


def test_init():
    """Test Argos translate models initialization"""
    assert len(argostranslatefiles.get_supported_formats()) >= 1
