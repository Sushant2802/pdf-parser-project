"""
Image extraction utilities using PyMuPDF (fitz).
Saves images to disk and returns metadata with relative paths.
Filters out very small images (logos/icons).
"""
import os
import hashlib
import logging
from typing import List, Dict, Any

log = logging.getLogger(__name__)

_seen_hashes = set()  # track unique images

def _hash_bytes(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()

def _save_image_bytes(image_bytes: bytes, out_path: str):
    with open(out_path, "wb") as f:
        f.write(image_bytes)

def extract_images_from_fitz_page(fitz_page, page_number: int, out_dir: str) -> List[Dict[str, Any]]:
    """
    Extracts images from a page, filters out duplicates & small logos.
    Returns list of dicts:
      {'path': 'output/images/page_001_img_1.png', 'bbox': (..), 'xref': int}
    """
    images_info = []
    doc = fitz_page.parent
    image_list = fitz_page.get_images(full=True)

    for idx, info in enumerate(image_list, start=1):
        xref = info[0]
        try:
            img_dict = doc.extract_image(xref)
            image_bytes = img_dict.get("image")
            image_ext = img_dict.get("ext", "png")

            # deduplicate by hash
            h = _hash_bytes(image_bytes)
            if h in _seen_hashes:
                continue
            _seen_hashes.add(h)

            # filter out tiny images (likely logos/icons)
            width, height = img_dict.get("width", 0), img_dict.get("height", 0)
            if width < 50 or height < 50:
                continue

            fname = f"page_{page_number:03d}_img_{idx}.{image_ext}"
            out_path = os.path.join(out_dir, fname)
            _save_image_bytes(image_bytes, out_path)

            # relative path
            rel_path = os.path.relpath(out_path, os.getcwd())

            images_info.append({
                "path": rel_path.replace("\\", "/"),
                "bbox": None,
                "xref": xref,
                "alt": img_dict.get("name") or ""
            })
        except Exception as e:
            log.warning("Failed to extract image xref=%s on page %d: %s", xref, page_number, e)

    return images_info
