#!/usr/bin/env python3
"""
Entry point for PDF -> structured JSON extraction.
Usage:
    python main.py --input path/to/pdf.pdf --output output/output.json --img-dir output/images
"""
import argparse
import json
import logging
import os
from pdf_reader import PDFParser

def setup_logging(debug: bool):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s | %(levelname)s | %(message)s")

def parse_args():
    parser = argparse.ArgumentParser(description="PDF to structured JSON extractor")
    parser.add_argument("--input", "-i", required=True, help="Input PDF file path")
    parser.add_argument("--output", "-o", default="output/output.json", help="Output JSON file path")
    parser.add_argument("--img-dir", "-m", default="output/images", help="Directory to save extracted images")
    parser.add_argument("--ocr", action="store_true", help="Enable OCR fallback for images (requires pytesseract)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--max-pages", type=int, default=None, help="Limit number of pages to parse (for testing)")
    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging(args.debug)
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    os.makedirs(args.img_dir, exist_ok=True)

    logging.info("Initializing PDF parser")
    parser = PDFParser(
        pdf_path=args.input,
        img_dir=args.img_dir,
        use_ocr=args.ocr,
    )

    logging.info("Starting parse...")
    result = parser.parse(max_pages=args.max_pages)

    logging.info("Writing output JSON to %s", args.output)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    logging.info("Done. Extracted %d pages", len(result.get("pages", [])))

if __name__ == "__main__":
    main()
