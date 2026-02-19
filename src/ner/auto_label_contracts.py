import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
contracts_dir = BASE_DIR / "data" / "processed_contracts"

TRAIN_DATA = []

def remove_overlaps(entities):
    entities = sorted(entities, key=lambda x: x[0])
    cleaned = []

    last_end = -1
    for start, end, label in entities:
        if start >= last_end:
            cleaned.append((start, end, label))
            last_end = end

    return cleaned


def find_spans(text, pattern, label):
    matches = []
    for match in re.finditer(pattern, text):
        start, end = match.span()
        matches.append((start, end, label))
    return matches


for file in contracts_dir.glob("*.txt"):
    text = file.read_text(encoding="utf-8")

    entities = []

    # MONEY
    entities += find_spans(text, r"\$\d{1,3}(,\d{3})*(\.\d+)?", "MONEY")

    # DATE (March 07, 2025)
    entities += find_spans(text, r"\b\w+ \d{1,2}, \d{4}\b", "DATE")

    # BORROWER
    borrower = re.search(r"BORROWER:\s*([A-Za-z\s]+),", text)
    if borrower:
        entities.append((borrower.start(1), borrower.end(1), "PARTY"))

    # LENDER
    lender = re.search(r"LENDER:\s*([A-Za-z\s\.]+),", text)
    if lender:
        entities.append((lender.start(1), lender.end(1), "PARTY"))

    # JURISDICTION
    entities += find_spans(text, r"Courts of [A-Za-z,\s]+", "JURISDICTION")

    entities = remove_overlaps(entities)

    TRAIN_DATA.append((text,{"entities": entities}))

print(f"Prepared {len(TRAIN_DATA)} contracts for training.")



