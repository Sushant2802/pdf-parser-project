"""
High-level PDF parsing orchestration.
"""

import logging
import os
from typing import List, Dict, Any, Optional

try:
    import fitz  # PyMuPDF
except Exception as e:
    raise ImportError("PyMuPDF (fitz) is required. pip install pymupdf") from e

try:
    import pdfplumber
except Exception as e:
    raise ImportError("pdfplumber is required. pip install pdfplumber") from e

from layout_analyzer import analyze_layout_blocks
from table_extractor import extract_tables_from_pdfplumber_page
from image_extractor import extract_images_from_fitz_page
from json_writer import build_page_content_entry
from utils import clean_text, detect_headers_footers

log = logging.getLogger(__name__)

class PDFParser:
    def __init__(self, pdf_path: str, img_dir: str = "output/images", use_ocr: bool = False):
        self.pdf_path = pdf_path
        self.img_dir = os.path.abspath(img_dir)
        self.use_ocr = use_ocr
        os.makedirs(self.img_dir, exist_ok=True)

    def parse(self, max_pages: Optional[int] = None) -> Dict[str, Any]:
        log.info("Opening PDF with PyMuPDF and pdfplumber: %s", self.pdf_path)
        doc = fitz.open(self.pdf_path)
        with pdfplumber.open(self.pdf_path) as pb:
            num_pages = len(doc)
            if max_pages:
                num_pages = min(num_pages, max_pages)

            page_texts = [doc.load_page(i).get_text("text") or "" for i in range(num_pages)]
            headers, footers = detect_headers_footers(page_texts)

            pages_output = []
            for i in range(num_pages):
                log.info("Parsing page %d/%d", i+1, num_pages)
                fitz_page = doc.load_page(i)
                pb_page = pb.pages[i] if i < len(pb.pages) else None

                page_result = self.parse_page(
                    page_number=i+1,
                    fitz_page=fitz_page,
                    pdfplumber_page=pb_page,
                    headers=headers,
                    footers=footers
                )
                pages_output.append(page_result)

        return {
            "source_file": os.path.basename(self.pdf_path),
            "num_pages": len(pages_output),
            "pages": pages_output
        }

    def parse_page(self, page_number: int, fitz_page, pdfplumber_page, headers, footers) -> Dict[str, Any]:
        blocks = fitz_page.get_text("dict").get("blocks", [])
        text_blocks = []
        for b in blocks:
            if b.get("type") == 0:
                spans = []
                for line in b.get("lines", []):
                    for span in line.get("spans", []):
                        spans.append({
                            "text": span.get("text", ""),
                            "bbox": tuple(span.get("bbox")),
                            "size": span.get("size"),
                            "flags": span.get("flags"),
                            "font": span.get("font"),
                        })
                block_text = " ".join([s["text"] for s in spans]).strip()
                if block_text:
                    text_blocks.append({
                        "text": block_text,
                        "spans": spans,
                        "bbox": b.get("bbox"),
                    })

        content_blocks = analyze_layout_blocks(text_blocks, headers=headers, footers=footers)

        tables = []
        if pdfplumber_page:
            try:
                extracted_tables = extract_tables_from_pdfplumber_page(pdfplumber_page)
                for t in extracted_tables:
                    if t and any(any(cell for cell in row) for row in t):
                        tables.append(t)
            except Exception as e:
                log.warning("pdfplumber table extraction failed on page %d: %s", page_number, str(e))

        images_info = []
        try:
            images_info = extract_images_from_fitz_page(fitz_page, page_number, self.img_dir)
        except Exception as e:
            log.warning("Image extraction failed on page %d: %s", page_number, str(e))

        page_content = []
        current_section = "General"

        for cb in content_blocks:
            if cb["type"] == "heading":
                current_section = cb["text"].strip()[:200] or "General"

            entry = build_page_content_entry(
                content_type=cb["type"],
                text=clean_text(cb.get("text", "")),
                section=current_section,
                sub_section=None,
                bbox=cb.get("bbox"),
                description=None
            )
            page_content.append(entry)

        for t_idx, t in enumerate(tables, start=1):
            entry = build_page_content_entry(
                content_type="table",
                table_data=t,
                section=current_section,
                sub_section=None,
                description=f"Table extracted by pdfplumber (table #{t_idx})"
            )
            page_content.append(entry)

        for img in images_info:
            entry = build_page_content_entry(
                content_type="chart",
                image_path=img.get("path"),
                section=current_section,
                sub_section=None,
                bbox=img.get("bbox"),
                description=img.get("alt") or None
            )
            page_content.append(entry)

        return {
            "page_number": page_number,
            "content": page_content,
        }
