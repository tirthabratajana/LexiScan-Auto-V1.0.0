import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
contracts_dir = BASE_DIR / "data" / "processed_contracts"

TRAIN_DATA = []

def remove_overlaps(entities):
    """
    Remove overlapping entities.
    Keeps the SHORTER span (more precise entity).
    """

    entities = sorted(entities, key=lambda x: (x[0], x[1] - x[0]))
    cleaned = []

    for start, end, label in entities:
        overlap = False

        for c_start, c_end, _ in cleaned:
            if not (end <= c_start or start >= c_end):
                overlap = True
                break

        if not overlap:
            cleaned.append((start, end, label))

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
    entities += find_spans(
        text,
        r"Courts of [A-Za-z\s]+,\s?[A-Z]{2}",
        "JURISDICTION"
    )

    entities = remove_overlaps(entities)

    TRAIN_DATA.append((text,{"entities": entities}))

print(f"Prepared {len(TRAIN_DATA)} contracts for training.")



