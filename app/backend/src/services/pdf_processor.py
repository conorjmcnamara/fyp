import io
import fitz
import re
from typing import Tuple


class PdfProcessorService:
    def extract_title_and_abstract(self, file_content: io.BytesIO) -> Tuple[str, str]:
        doc = fitz.open(stream=file_content, filetype="pdf")
        first_page = doc[0]
        text_blocks = first_page.get_text("dict")["blocks"]
        
        title_lines = []
        abstract_lines = []
        abstract_started = False
        max_font_size = 0

        for block in text_blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_size = span["size"]
                        if font_size > max_font_size:
                            max_font_size = font_size

        for block in text_blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()

                        # Extract title assuming it has the largest font size
                        if span["size"] == max_font_size:
                            title_lines.append(text)

                        # Detect "Abstract" to start collecting text
                        if re.match(r"^abstract\b", text, re.IGNORECASE):
                            abstract_started = True
                            continue
                        
                        # Stop collecting abstract text when reach another major section
                        if abstract_started:
                            if re.match(
                                r"^(keywords?|1\.|introduction|background?)\b",
                                text,
                                re.IGNORECASE
                            ):
                                abstract_started = False
                            else:
                                abstract_lines.append(text)

        title = " ".join(title_lines) if title_lines else None
        abstract = " ".join(abstract_lines) if abstract_lines else None
        return title, abstract