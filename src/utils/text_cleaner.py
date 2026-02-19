import re


def normalize_whitespace(text: str) -> str:
    """
    Replace multiple spaces, tabs, and newlines with a single space.
    This ensures consistent token boundaries for NLP models.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def remove_page_numbers(text: str) -> str:
    """
    Remove page numbers ONLY if they appear alone on a line.
    Example:
        1
        2
    But keep numbers inside sentences.
    """
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        stripped = line.strip()

        # Remove line if it contains ONLY digits (page number)
        if stripped.isdigit():
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def fix_broken_hyphenated_words(text: str) -> str:
    """
    Fix words broken across lines due to OCR.
    Example:
        agree-
        ment
    becomes:
        agreement
    """
    # Remove hyphen + newline between split words
    text = re.sub(r"-\s*\n\s*", "", text)
    return text


def standardize_currency(text: str) -> str:
    """
    Standardize different currency formats into a consistent format.
    Example:
        USD 500,000
        500000 USD
        $ 500000
    → $500000
    """
    # Convert USD formats to $
    text = re.sub(r"\bUSD\s*", "$", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*USD\b", "", text, flags=re.IGNORECASE)

    # Remove spaces between currency symbol and number
    text = re.sub(r"\$\s+", "$", text)

    return text


def remove_repeated_headers(text: str) -> str:
    """
    Remove repeated headers appearing on every page.
    Example:
        SERVICE AGREEMENT
        SERVICE AGREEMENT
        SERVICE AGREEMENT
    Keeps only first occurrence.
    """
    lines = text.split("\n")
    seen = set()
    cleaned_lines = []

    for line in lines:
        line_stripped = line.strip()

        # If line appears multiple times and is short (likely header), remove duplicates
        if line_stripped in seen and len(line_stripped) < 50:
            continue

        seen.add(line_stripped)
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def apply_lowercase(text: str, lowercase: bool = False) -> str:
    """
    Optional lowercasing.
    IMPORTANT:
    Keep False for legal documents if capitalization matters.
    """
    return text.lower() if lowercase else text


def remove_repeated_clauses(text: str) -> str:
    """
    Keeps only first full clause block.
    Removes repeated clause sections from later pages.
    """

    # Find first occurrence of CLAUSE ONE
    first_index = text.find("CLAUSE ONE")

    if first_index == -1:
        return text  # no clause found

    # Find second occurrence
    second_index = text.find("CLAUSE ONE", first_index + 1)

    if second_index == -1:
        return text  # no repetition

    # Keep everything before second occurrence
    return text[:second_index]

def remove_duplicate_lines(text: str) -> str:
    """
    Remove duplicate lines while preserving order.
    More reliable than sentence splitting.
    """

    lines = text.split("\n")
    seen = set()
    cleaned_lines = []

    for line in lines:
        normalized = line.strip()

        if not normalized:
            continue

        # Normalize whitespace for comparison
        normalized = " ".join(normalized.split())

        if normalized not in seen:
            seen.add(normalized)
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)




def clean_text(text: str, lowercase: bool = False) -> str:
    """
    Master cleaning pipeline.
    Applies all preprocessing steps in correct order.
    """

    # Step 1: Fix word breaks before altering whitespace
    text = fix_broken_hyphenated_words(text)

    # Step 2: Remove page artifacts
    text = remove_page_numbers(text)
    text = remove_repeated_headers(text)

    # Step 3: Standardize structured patterns
    text = standardize_currency(text)

    # Step 4: Normalize whitespace
    text = normalize_whitespace(text)

    # Step 5: Optional lowercasing
    text = apply_lowercase(text, lowercase=lowercase)

    # Step 6: remove repeated clause section
    text = remove_repeated_clauses(text)

    text = remove_duplicate_lines(text)


    return text
