from argostranslatefiles.abstract_file import AbstractFile
import zipfile
import bs4
from bs4 import BeautifulSoup
from bs4.element import NavigableString

import argostranslate
from argostranslate import translate
from argostranslate.tags import Tag, translate_tags


class AbstractXml(AbstractFile):
    def itag_of_soup(self, soup):
        """Returns an argostranslate.tags.ITag tree from a BeautifulSoup object.
        Args:
            soup (bs4.element.Navigablestring or bs4.element.Tag): Beautiful Soup object
        Returns:
            argostranslate.tags.ITag: Argos Translate ITag tree
        """
        if isinstance(soup, bs4.element.NavigableString):
            return str(soup)

        translateable = soup.text != ""
        to_return = Tag([self.itag_of_soup(content) for content in soup.contents], translateable)
        to_return.soup = soup
        return to_return

    def soup_of_itag(self, itag):
        """Returns a BeautifulSoup object from an Argos Translate ITag.
        Args:
            itag (argostranslate.tags.ITag): ITag object to convert to Soup
        Returns:
            bs4.elements.BeautifulSoup: BeautifulSoup object
        """
        if type(itag) == str:
            return bs4.element.NavigableString(itag)
        soup = itag.soup
        soup.contents = [self.soup_of_itag(child) for child in itag.children]
        return soup
