from pathlib import Path
import re


def merge_contract_pages():
    BASE_DIR = Path(__file__).resolve().parents[2]
    ocr_dir = BASE_DIR / "data" / "ocr_text"
    output_dir = BASE_DIR / "data" / "processed_contracts"
    output_dir.mkdir(exist_ok=True)

    txt_files = sorted(ocr_dir.glob("*.txt"))

    contracts = {}

    for file in txt_files:
        # Extract contract name before _page_
        match = re.match(r"(.*)_page_\d+", file.stem)
        if not match:
            continue

        contract_name = match.group(1)

        if contract_name not in contracts:
            contracts[contract_name] = ""

        contracts[contract_name] += file.read_text(encoding="utf-8") + "\n"

    for contract_name, text in contracts.items():
        output_path = output_dir / f"{contract_name}.txt"
        output_path.write_text(text, encoding="utf-8")

    print("✅ Contracts merged successfully.")

if __name__ == "__main__":
    merge_contract_pages()