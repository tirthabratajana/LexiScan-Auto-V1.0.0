LexiScan Auto

Project 2 – Intelligent Document Parsing (NLP / NER)
Infotact Solutions – Production ML Track

📌 Overview

LexiScan Auto is a production-oriented Named Entity Recognition (NER) system designed to extract structured entities from unstructured legal contracts.

Target Entities:

Effective Date

Termination Date

Party Names

Monetary Values

Jurisdiction

✅ Week 1 – OCR Pipeline & Annotation
Objective

Prepare clean and structured training data.

Tasks Completed

Built PDF to Image conversion pipeline

Implemented OCR using Tesseract

Applied basic image preprocessing

Cleaned extracted text

Manually annotated contracts (BIO tagging format)

Output

Clean text files from scanned PDFs

Annotated dataset ready for NER training

✅ Week 2 – NER Modeling
Objective

Train a custom Named Entity Recognition model.

Tasks Completed

Converted annotations to training format

Split dataset (Train/Test)

Trained custom SpaCy NER model

Evaluated using Precision, Recall, F1-score

Saved trained model artifact

Evaluation Metric

F1-Score (Primary)
