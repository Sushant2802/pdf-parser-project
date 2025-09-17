"""
Helpers to build JSON entries consistently with assignment schema.
"""

from typing import Any, Dict, List, Optional

def build_page_content_entry(content_type: str,
                             text: Optional[str] = None,
                             table_data: Optional[List[List[Any]]] = None,
                             image_path: Optional[str] = None,
                             section: Optional[str] = None,
                             sub_section: Optional[str] = None,
                             bbox: Optional[Any] = None,
                             description: Optional[str] = None) -> Dict[str, Any]:
    """
    Build a JSON entry for a single content block.
    Matches assignment-required schema.
    """
    entry: Dict[str, Any] = {
        "type": content_type,           # paragraph | heading | table | chart
        "section": section or "General",
        "sub_section": sub_section      # can be None
    }

    if content_type in ("paragraph", "heading") and text:
        entry["text"] = text

    if content_type == "table":
        entry["table_data"] = table_data or []
        entry["description"] = description or None

    if content_type == "chart":
        entry["image_path"] = image_path or None
        entry["description"] = description or None

    if bbox:
        entry["bbox"] = bbox

    return entry
