# PDF Parser Project

## 📌 Overview
This project is a **PDF Parsing and Structured JSON Extraction Tool**.  
It processes PDF files and extracts their content into a **clean, hierarchical JSON format**.  
The parser is capable of detecting **headings, paragraphs, tables, and charts/images** while maintaining the page structure and document hierarchy.

---

## 📂 Project Structure
```
pdf_parser_project/
│
├── main.py                 # Entry point (runs the complete pipeline)
├── pdf_reader.py           # Reads PDF pages (text and raw blocks)
├── layout_analyzer.py      # Identifies headings, sections, and paragraphs
├── table_extractor.py      # Extracts tables from PDF
├── image_extractor.py      # Extracts charts/images from PDF
├── json_writer.py          # Builds and writes the final structured JSON
├── utils.py                # Helper functions (cleaning, preprocessing)
│
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── output/
│   ├── output.json         # Final structured JSON file
│   └── images/             # Extracted charts and images
│
└── tests/
    └── validate_json.py    # Script to validate JSON format
```

---

## ⚙️ Installation
Clone the repository and install dependencies:
```bash
git clone <repo_url>
cd pdf_parser_project
pip install -r requirements.txt
```

---

## ▶️ Usage
Run the parser with:
```bash
python main.py --input <path_to_pdf> --output ./output/output.json
```

Example:
```bash
python main.py --input sample.pdf --output ./output/output.json
```

---

## 📑 Output Format
The output is a structured JSON file (`output/output.json`) along with extracted images stored in `output/images/`.

Example JSON snippet:
```json
{
  "source_file": "test_file.pdf",
  "num_pages": 17,
  "pages": [
    {
      "page_number": 1,
      "content": [
        {
          "type": "heading",
          "section": "MONTHLY FACTSHEET",
          "text": "MONTHLY FACTSHEET"
        },
        {
          "type": "chart",
          "section": "MONTHLY FACTSHEET",
          "image_path": "output/images/page_001_img_1.jpeg"
        }
      ]
    }
  ]
}
```

---

## ✅ Validation
To ensure the JSON is valid and correctly structured:
```bash
python tests/validate_json.py ./output/output.json
```

---

## 📊 Features
- Page-wise text extraction  
- Section and sub-section detection  
- Table extraction with structured data  
- Chart and image extraction (saved separately)  
- Clean hierarchical JSON output  

---

## 📌 Evaluation Criteria (from assignment)
- Accuracy of extracted content  
- Correctness of JSON structure and hierarchy  
- Code quality and modularity  

---

## 📝 License
This project is developed for educational and assignment purposes. You are free to modify and extend it for your use.
