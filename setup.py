from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required_packages = f.read().splitlines()

with open("README.md") as f:
    long_description = f.read()

setup(
    name="argos-translate-files",
    version="1.4.0",
    description="Translate files with Argos Translate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="S. Thuret",
    author_email="contact@sebastien-thuret.fr",
    url="https://github.com/LibreTranslate/argos-translate-files",
    packages=find_packages(),
    install_requires=required_packages,
)
