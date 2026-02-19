import pytesseract
import cv2
from pathlib import Path

# Removes background noise
# Enhances text contrast
# Makes OCR more stable

# Image Preprocessing
def preprocess_image(image_path: str):
    # Read image using OpenCV
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    # Use adaptive threshold instead of fixed
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh


def image_to_text(image_path: str) -> str:
    processed_img = preprocess_image(image_path)

    text = pytesseract.image_to_string(
        processed_img,
        lang="eng",
        config="--psm 6"
    )

    return text


def save_text(text: str, image_path: str):
    BASE_DIR = Path(__file__).resolve().parents[2]
    output_dir = BASE_DIR / "data" / "ocr_text"
    output_dir.mkdir(parents=True, exist_ok=True)

    image_name = Path(image_path).stem
    text_file_path = output_dir / f"{image_name}.txt"

    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(text)

    return str(text_file_path)
