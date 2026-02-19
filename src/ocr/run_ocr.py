from pathlib import Path
import re

from pdf_to_image import pdf_to_images
from image_to_text import image_to_text
from src.utils.text_cleaner import clean_text


def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0


def merge_pages_dynamically(page_texts):
    """
    Merge pages while removing repeated clause blocks.
    Keeps:
        - Full first occurrence of clauses
        - Footer/signature content
    """

    full_text = "\n".join(page_texts)

    # Find all positions of "CLAUSE ONE"
    clause_positions = []
    start = 0

    while True:
        idx = full_text.find("CLAUSE ONE", start)
        if idx == -1:
            break
        clause_positions.append(idx)
        start = idx + 1

    # If only one occurrence → no repetition
    if len(clause_positions) <= 1:
        return full_text

    # Keep everything up to second occurrence
    first_block_end = clause_positions[1]
    cleaned_text = full_text[:first_block_end]

    # Append footer content after last clause block
    last_clause_position = clause_positions[-1]
    footer = full_text[last_clause_position:]

    # Remove repeated clause text from footer
    footer = re.sub(r"CLAUSE ONE.*?CLAUSE EIGHT.*?(?=New|\Z)", "", footer, flags=re.DOTALL)

    return cleaned_text + "\n" + footer.strip()


def process_all_pdfs():
    BASE_DIR = Path(__file__).resolve().parents[2]

    raw_pdf_dir = BASE_DIR / "data" / "raw_pdfs"
    output_dir = BASE_DIR / "data" / "processed_contracts"
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(
        raw_pdf_dir.glob("*.pdf"),
        key=lambda x: extract_number(x.stem)
    )

    if not pdf_files:
        print("❌ No PDFs found.")
        return

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")

        image_paths = pdf_to_images(str(pdf_path))

        page_texts = []

        for img in image_paths:
            raw_text = image_to_text(img)
            cleaned_text = clean_text(raw_text, lowercase=False)
            page_texts.append(cleaned_text)

        # Keep first page fully
        full_contract_text = page_texts[0]

        # Detect footer dynamically using DATE pattern
        date_pattern = r"\b\w+ \d{1,2}, \d{4}\b"

        for page in page_texts[1:]:
            match = re.search(date_pattern, page)
            if match:
                full_contract_text += "\n" + page[match.start():]

        # 🔥 DEFINE output_file HERE
        output_file = output_dir / f"{pdf_path.stem}.txt"

        output_file.write_text(full_contract_text.strip(), encoding="utf-8")

        print(f"✅ Saved merged contract: {output_file.name}")

    print("🎉 All contracts processed successfully.")



if __name__ == "__main__":
    process_all_pdfs()
