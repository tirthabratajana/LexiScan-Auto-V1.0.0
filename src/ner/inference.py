import re

import spacy
from pathlib import Path
from src.ocr.pdf_to_image import pdf_to_images
from src.ocr.image_to_text import image_to_text
from src.utils.text_cleaner import clean_text

BASE_DIR = Path(__file__).resolve().parents[2]

def extract_entities_from_pdf(pdf_path):

    model_path = BASE_DIR / "data" / "models" / "trained_ner_model"

    nlp = spacy.load(model_path)

    image_paths = pdf_to_images(str(pdf_path))

    page_texts = []

    for img in image_paths:
        raw_text = image_to_text(img)
        cleaned_text = clean_text(raw_text, lowercase=False)
        page_texts.append(cleaned_text)

    # 🔥 Use same merge logic as training
    full_text = page_texts[0]

    date_pattern = r"\b\w+ \d{1,2}, \d{4}\b"

    for page in page_texts[1:]:
        match = re.search(date_pattern, page)
        if match:
            full_text += "\n" + page[match.start():]

    doc = nlp(full_text)

    extracted = {}

    for ent in doc.ents:
        extracted.setdefault(ent.label_, set()).add(ent.text)

    return {k: list(v) for k, v in extracted.items()}


if __name__ == "__main__":
    pdf_path = BASE_DIR / "data" / "raw_pdfs" / "sample_contract.pdf"

    results = extract_entities_from_pdf(pdf_path)

    print("\nExtracted Entities:")
    print(results)