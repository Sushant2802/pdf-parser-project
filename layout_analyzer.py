
"""
Analyze text blocks (from PyMuPDF) to decide headings / subheadings / paragraphs.
Relies on font size heuristics and repeated header/footer removal.
"""
import statistics
from typing import List, Dict, Any, Optional

def analyze_layout_blocks(blocks: List[Dict[str, Any]],
                          headers: Optional[List[str]] = None,
                          footers: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Input:
      blocks: list of {'text':..., 'spans':[{'text','size',...}], 'bbox': ...}
      headers/footers: lists of strings to ignore
    Output:
      list of content blocks like {'type': 'heading'|'paragraph', 'text':..., 'section':..., 'bbox':...}
    """
    if headers is None:
        headers = []
    if footers is None:
        footers = []

    # Flatten sizes
    all_sizes = []
    for b in blocks:
        for s in b.get("spans", []):
            size = s.get("size")
            if size:
                all_sizes.append(size)
    median_size = statistics.median(all_sizes) if all_sizes else 10.0

    results = []
    for b in blocks:
        text = b.get("text", "").strip()
        if not text:
            continue
        # Skip if matches header/footer candidates
        if any(h.strip() and h.strip() in text for h in headers):
            continue
        if any(f.strip() and f.strip() in text for f in footers):
            continue

        # compute average size for block
        sizes = [s.get("size") for s in b.get("spans", []) if s.get("size")]
        avg_size = sum(sizes) / len(sizes) if sizes else median_size

        # classify: if avg_size significantly larger than median -> heading
        if avg_size >= median_size * 1.2:
            ctype = "heading"
            # heuristic for section name = heading text
            section = text.strip()[:240]
        else:
            ctype = "paragraph"
            section = None

        results.append({
            "type": ctype,
            "text": text,
            "section": section,
            "bbox": b.get("bbox")
        })
    return results
