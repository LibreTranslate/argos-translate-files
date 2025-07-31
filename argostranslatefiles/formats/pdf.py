import pymupdf as fitz
from typing import List
from argostranslate.translate import ITranslation
from argostranslatefiles.abstract_file import AbstractFile


class Pdf(AbstractFile):   
    supported_file_extensions = ['.pdf']

    def translate(self, underlying_translation: ITranslation, file_path: str) -> str:
        outfile_path = self.get_output_path(underlying_translation, file_path)
        
        translator = PdfTranslator(
            pdf_path=file_path,
            output_path=outfile_path,
            underlying_translation=underlying_translation
        )
        translator.translate_pdf()
        
        return outfile_path
    

    def get_texts(self, file_path: str):
        doc = fitz.open(file_path)

        texts = []

        count = 0
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text = page.get_text().strip()
            if text:
                count += len(text)
                texts.append(text)
                if count >= 4096:
                    break
        
        doc.close()
        return " ".join(texts)[:4096]


# Roughly based on https://github.com/CBIhalsen/PolyglotPDF/blob/main/main.py
# which is GPLv3
class PdfTranslator:    
    def __init__(self, pdf_path: str, output_path: str, underlying_translation: ITranslation):
        self.pdf_path = pdf_path
        self.output_path = output_path
        self.underlying_translation = underlying_translation
        self.doc = fitz.open(pdf_path)
        self.pages_data = []


    def translate_pdf(self):
        self._extract_text_from_pages()
        self._translate_pages_data()
        self._apply_translations_to_pdf()
        self._save_translated_pdf()
    

    def _decimal_to_hex_color(self, decimal_color):
        if decimal_color == 0:
            return '#000000'
        hex_color = hex(decimal_color)[2:]
        hex_color = hex_color.zfill(6)
        return f'#{hex_color}'


    def _is_math(self, text, page_num, font_info):
        #I assume this is a placeholder that's going to be implemented later in the polyglotPDF/main.py later on, I'm leaving this here if it is implemented later copy pasting that code should work fine. Same for is_non_text.
        return False


    def _is_non_text(self, text):
        return False


    def _extract_text_from_pages(self):
        # The reason for separating _extract_text_from_pages and _extract_text_with_pymupdf is later if _extract_using_OCR is implemented, it can just go here. 
        page_count = self.doc.page_count
        for page_num in range(page_count):
            self._extract_text_with_pymupdf(page_num)
    

    def _extract_text_with_pymupdf(self, page_num: int):
        while len(self.pages_data) <= page_num:
            self.pages_data.append([])
        
        page = self.doc.load_page(page_num)
        
        links = page.get_links()
        link_map = {}
        for link in links:
            rect = fitz.Rect(link["from"])
            link_map[rect] = {
                "uri": link.get("uri", ""),
                "page": link.get("page", -1),
                "to": link.get("to", None),
                "kind": link.get("kind", 0)
            }
        
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span.get("text", "").strip()
                        if text and not self._is_math(text, page_num, None) and not self._is_non_text(text):
                            bbox = span.get("bbox", (0, 0, 0, 0))
                            font_size = span.get("size", 12)
                            font_flags = span.get("flags", 0)
                            color = span.get("color", 0)
                            is_bold = bool(font_flags & 2**4)
                            span_rect = fitz.Rect(bbox)
                            link_info = None
                            for link_rect, link_data in link_map.items():
                                if span_rect.intersects(link_rect):
                                    link_info = link_data
                                    break
                            
                            self.pages_data[page_num].append([
                                text,
                                tuple(bbox),
                                None,  # Translation placeholder
                                0,     # Angle (rotation)
                                self._decimal_to_hex_color(color),
                                0,     # Text indent
                                is_bold,
                                font_size,
                                link_info  # Link information
                            ])

    
    def _translate_pages_data(self):
        try:
            for page_blocks in self.pages_data:
                for block in page_blocks:
                    original_text = block[0]
                    translated_text = self.underlying_translation.translate(original_text)
                    block[2] = translated_text
        except Exception as e:
            # Fallback: use original text in case of math or any other issues
            for page_blocks in self.pages_data:
                for block in page_blocks:
                    block[2] = block[0]

    
    def _apply_translations_to_pdf(self):        
        for page_index, blocks in enumerate(self.pages_data):
            if not blocks:
                continue
                
            page = self.doc.load_page(page_index)
            
            normal_blocks = []
            bold_blocks = []
            
            for block in blocks:
                coords = block[1]
                translated_text = block[2] if block[2] is not None else block[0]
                
                # Calculate expansion factor based on text length ratio
                len_ratio = min(1.05, max(1.01, len(translated_text) / max(1, len(block[0]))))
                
                x0, y0, x1, y1 = coords
                width = x1 - x0
                height = y1 - y0
                
                # Expand horizontally to accommodate longer text
                h_expand = (len_ratio - 1) * width
                x1 = x1 + h_expand
                
                # Reduce vertical coverage to be more precise
                vertical_margin = min(height * 0.1, 3)
                y0 = y0 + vertical_margin
                y1 = y1 - vertical_margin
                
                # Ensure minimum height
                if y1 - y0 < 10:
                    y_center = (coords[1] + coords[3]) / 2
                    y0 = y_center - 5
                    y1 = y_center + 5
                
                enlarged_coords = (x0, y0, x1, y1)
                rect = fitz.Rect(*enlarged_coords)
                
                # Cover original text with white rectangle
                try:
                    page.add_redact_annot(rect)
                    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
                except Exception:
                    page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                
                is_bold = len(block) > 6 and block[6]
                if is_bold:
                    bold_blocks.append((block, enlarged_coords))
                else:
                    normal_blocks.append((block, enlarged_coords))
            
            self._insert_styled_text_blocks(page, normal_blocks, is_bold=False)
            self._insert_styled_text_blocks(page, bold_blocks, is_bold=True)
    

    def _insert_styled_text_blocks(self, page, blocks: List, is_bold: bool):
        if not blocks:
            return
        
        font_weight = "bold" if is_bold else "normal"
        
        for block_data in blocks:
            block, enlarged_coords = block_data
            translated_text = block[2] if block[2] is not None else block[0]
            angle = block[3] if len(block) > 3 else 0
            color = block[4] if len(block) > 4 else '#000000'
            text_indent = block[5] if len(block) > 5 else 0
            font_size = block[7] if len(block) > 7 else 12
            link_info = block[8] if len(block) > 8 else None
            
            rect = fitz.Rect(*enlarged_coords)
            
            if link_info:
                if link_info.get("uri"):
                    translated_text = f'<a href="{link_info["uri"]}" style="color: {color}; text-decoration: underline;">{translated_text}</a>'
                elif link_info.get("page", -1) >= 0:
                    page_num = link_info["page"]
                    translated_text = f'<a href="#page{page_num}" style="color: {color}; text-decoration: underline;">{translated_text}</a>'
            
            css = f"""
            * {{
                color: {color};
                font-weight: {font_weight};
                font-size: {font_size}px;
                text-indent: {text_indent}pt;
                line-height: 1.2;
                word-wrap: break-word;
                overflow-wrap: break-word;
                width: 100%;
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            a {{
                text-decoration: underline;
            }}
            """
            
            html_content = f'<div style="font-size: {font_size}px; color: {color}; font-weight: {font_weight}; text-indent: {text_indent}pt; line-height: 1.2; word-wrap: break-word;">{translated_text}</div>'
            
            try:
                page.insert_htmlbox(rect, html_content, css=css, rotate=angle)
                
                if link_info:
                    self._add_link_annotation(page, rect, link_info)
                    
            except Exception as e:
                page.insert_text(rect.tl, translated_text, fontsize=font_size)
                
                if link_info:
                    self._add_link_annotation(page, rect, link_info)

    
    def _add_link_annotation(self, page, rect, link_info):
        try:
            link_dict = {
                "kind": link_info.get("kind", 1),  # 1 = URI link, 2 = GoTo link
                "from": rect
            }
            
            if link_info.get("uri"):
                link_dict["uri"] = link_info["uri"]
                link_dict["kind"] = 1  # URI link
            elif link_info.get("page", -1) >= 0:
                link_dict["page"] = link_info["page"]
                link_dict["kind"] = 2
                if link_info.get("to"):
                    link_dict["to"] = link_info["to"]
            
            page.insert_link(link_dict)
        except Exception as e:
            pass

    
    def _save_translated_pdf(self):
        new_doc = fitz.open()
        new_doc.insert_pdf(self.doc)
        new_doc.save(self.output_path, garbage=4, deflate=True)
        new_doc.close()
        self.doc.close()