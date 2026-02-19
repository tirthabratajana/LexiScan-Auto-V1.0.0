from pdf2image import convert_from_path
from pathlib import Path


def pdf_to_images(pdf_path: str):
    BASE_DIR = Path(__file__).resolve().parents[2]
    output_dir = BASE_DIR / "data" / "ocr_images"
    output_dir.mkdir(parents=True, exist_ok=True)

    images = convert_from_path(pdf_path, dpi=300)

    image_paths = []

    for i, image in enumerate(images):
        img_path = output_dir / f"{Path(pdf_path).stem}_page_{i+1}.png"
        image.save(img_path, "PNG")
        image_paths.append(str(img_path))

    return image_paths
