import argostranslate
import bs4
from argostranslate.tags import Tag, ITag

from argostranslatefiles.abstract_file import AbstractFile


class AbstractXml(AbstractFile):

    def is_translatable(self, soup):
        return soup.text != ""

    def itag_of_soup(self, soup):
        """Returns an argostranslate.tags.ITag tree from a BeautifulSoup object.
        Args:
            soup (bs4.element.Navigablestring or bs4.element.Tag): Beautiful Soup object
        Returns:
            argostranslate.tags.ITag: Argos Translate ITag tree
        """
        if isinstance(soup, bs4.element.NavigableString):
            return str(soup)

        translatable = self.is_translatable(soup)
        to_return = Tag([self.itag_of_soup(content) for content in soup.contents], translatable)
        to_return.soup = soup
        return to_return

    def soup_of_itag(self, itag: ITag):
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
