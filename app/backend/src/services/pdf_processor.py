import io
import fitz
import re
from typing import Tuple

class PdfProcessorService:
    def extract_title_and_abstract(self, file_content: io.BytesIO) -> Tuple[str, str]:
        doc = fitz.open(stream=file_content, filetype="pdf")
        
        first_page = doc[0]  # Process only the first page

        # Extract text blocks with font properties
        blocks = first_page.get_text("dict")["blocks"]
        
        title_lines = []
        abstract_lines = []
        abstract_started = False
        font_sizes = []

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_sizes.append(span["size"])

        max_font_size = max(font_sizes) if font_sizes else 0  # Largest font size on page

        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        font_size = span["size"]

                        # Capture title (largest font size)
                        if font_size == max_font_size:
                            title_lines.append(text)

                        # Detect "Abstract" and start collecting text
                        if re.match(r"^abstract\b", text, re.IGNORECASE):
                            abstract_started = True
                            continue  # Skip "Abstract" heading itself
                        
                        # Stop when reaching another major section
                        if abstract_started:
                            if re.match(r"^(keywords?|1\.|introduction|background|methods?)\b", text, re.IGNORECASE):
                                abstract_started = False
                            else:
                                abstract_lines.append(text)

        title = " ".join(title_lines) if title_lines else "Title not found"
        abstract = " ".join(abstract_lines) if abstract_lines else "Abstract not found"

        return title, abstract