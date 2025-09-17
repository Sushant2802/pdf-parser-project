"""
Table extraction utilities (pdfplumber-based).
"""
from typing import List
import logging

log = logging.getLogger(__name__)

def extract_tables_from_pdfplumber_page(pb_page) -> List[List[List[str]]]:
    """
    Uses pdfplumber's extract_tables (a heuristics-based extractor).
    Returns list of tables where each table is a list of rows (list of cell strings).
    """
    tables = []
    # pdfplumber has two useful methods: extract_table (single) and extract_tables (list)
    try:
        raw_tables = pb_page.extract_tables()
        if raw_tables:
            for rt in raw_tables:
                # Clean rows: convert None -> "" and strip
                cleaned = []
                for row in rt:
                    cleaned_row = [ (cell.strip() if isinstance(cell, str) else (str(cell).strip() if cell not in (None,) else "")) for cell in row ]
                    cleaned.append(cleaned_row)
                tables.append(cleaned)
    except Exception as e:
        log.warning("pdfplumber.extract_tables threw an error: %s", e)
        # fallback: try a looser extraction if available
        try:
            table = pb_page.extract_table()
            if table:
                cleaned = []
                for row in table:
                    cleaned_row = [ (cell.strip() if isinstance(cell, str) else (str(cell).strip() if cell not in (None,) else "")) for cell in row ]
                    cleaned.append(cleaned_row)
                tables.append(cleaned)
        except Exception as e2:
            log.warning("pdfplumber.extract_table fallback failed: %s", e2)
    return tables
