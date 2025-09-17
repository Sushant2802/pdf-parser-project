"""
Utility helpers: text cleaning, header/footer detection, hyphen handling.
"""
import re
from typing import List, Tuple, Optional

def clean_text(text: str) -> str:
    """Do some light cleaning: fix hyphenations, normalize whitespace."""
    if not text:
        return ""
    s = text.replace("\r", " ").replace("\n", " ")
    # fix hyphenation at line breaks: e.g., "multi-\nline" -> "multiline"
    s = re.sub(r"(\w)-\s+(\w)", r"\1\2", s)
    # multiple spaces to single
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()

def detect_headers_footers(page_texts: List[str]) -> Tuple[List[str], List[str]]:
    """
    Heuristic detection of repeating header/footer lines.
    Returns (headers_list, footers_list).
    Approach:
      - for each page, take the first N chars/first line as header candidate
      - for footer, take last line
      - count frequency across pages, return those which appear on >= 30% pages
    """
    from collections import Counter
    header_candidates = []
    footer_candidates = []
    for t in page_texts:
        if not t:
            continue
        lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
        if not lines:
            continue
        header_candidates.append(lines[0][:200])
        footer_candidates.append(lines[-1][:200])

    def frequent(cands):
        c = Counter(cands)
        threshold = max(1, int(len(page_texts) * 0.3))  # present in at least 30% pages
        return [item for item, cnt in c.items() if cnt >= threshold]

    headers = frequent(header_candidates)
    footers = frequent(footer_candidates)
    return headers, footers
