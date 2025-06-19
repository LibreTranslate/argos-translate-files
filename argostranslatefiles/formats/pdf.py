from argostranslate.translate import ITranslation
from translatehtml import translate_html
from argostranslatefiles.abstract_file import AbstractFile
import pymupdf

class Pdf(AbstractFile):
    supported_file_extensions = ['.pdf']

    def translate(self, underlying_translation: ITranslation, file_path: str):
        outfile_path = self.get_output_path(underlying_translation, file_path)

        infile = pymupdf.open(file_path)

        outfile = pymupdf.DocumentWriter(outfile_path)
        
        for page in infile:
            full_html = page.get_text("html")
            translated_page = translate_html(underlying_translation, full_html)
            story = pymupdf.Story(html=translated_page)
            # Use the original page's dimensions as the new page size
            page_rect = page.rect  # page.rect is the page's rectangle (size):contentReference[oaicite:3]{index=3}
            # Place and render the story content onto one or more pages of this size
            more = True
            while more:
                device = outfile.begin_page(page_rect)        # start a new output page
                more, _ = story.place(page_rect)             # flow content into the page area
                story.draw(device)                           # render the placed content on the page
                outfile.end_page() 

        infile.close()
        outfile.close()  # save and close the output PDF

        return outfile_path

    def get_texts(self, file_path: str):
        doc = pymupdf.open(file_path)
        texts = []
        for page in doc:
            texts.append(page.get_text())
        return texts