"""
Simple JSON validator for the produced output format.
Run: python tests/validate_json.py output/output.json
"""
import sys
import json
from typing import Any

def validate(data: Any) -> bool:
    if not isinstance(data, dict):
        print("Top-level must be dict")
        return False
    if "pages" not in data or not isinstance(data["pages"], list):
        print("Missing pages list")
        return False
    for p in data["pages"]:
        if "page_number" not in p or "content" not in p:
            print("Each page must have page_number and content")
            return False
        if not isinstance(p["content"], list):
            print("page.content must be a list")
            return False
        for c in p["content"]:
            if "type" not in c:
                print("Each content item must have type")
                return False
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_json.py path/to/output.json")
        sys.exit(2)
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    ok = validate(data)
    print("VALID" if ok else "INVALID")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
