import json
import random
from pathlib import Path
import json
import spacy
from spacy.training.example import Example
from sklearn.model_selection import train_test_split
from spacy.scorer import Scorer
from spacy.training import Example

from auto_label_contracts import TRAIN_DATA

def save_dataset(train_data, test_data):
    BASE_DIR = Path(__file__).resolve().parents[1]
    dataset_dir = BASE_DIR / "data" / "datasets"
    dataset_dir.mkdir(parents=True, exist_ok=True)

    train_path = dataset_dir / "train_data.json"
    test_path = dataset_dir / "test_data.json"

    with open(train_path, "w", encoding="utf-8") as f:
        json.dump(train_data, f, indent=4)

    with open(test_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f, indent=4)

    print(f"✅ Train data saved to: {train_path}")
    print(f"✅ Test data saved to: {test_path}")

def evaluate_model(nlp, test_data):
    scorer = Scorer()

    examples = []

    for text, annotations in test_data:
        doc = nlp(text)
        example = Example.from_dict(doc, annotations)
        examples.append(example)

    scores = scorer.score(examples)

    print("\n📊 Evaluation Metrics:")
    print("Precision:", scores["ents_p"])
    print("Recall:", scores["ents_r"])
    print("F1 Score:", scores["ents_f"])


def train_model(train_data, test_data, n_iter=30):

    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")

    # Add labels
    for _, annotations in train_data:
        for ent in annotations["entities"]:
            ner.add_label(ent[2])

    optimizer = nlp.begin_training()

    for iteration in range(n_iter):
        random.shuffle(train_data)
        losses = {}

        for text, annotations in train_data:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.2, losses=losses)

        print(f"Iteration {iteration+1}, Loss: {losses}")

    return nlp


if __name__ == "__main__":

    train_data, test_data = train_test_split(TRAIN_DATA, test_size=0.2, random_state=42)

    save_dataset(train_data, test_data)

    model = train_model(train_data, test_data)

    evaluate_model(model, test_data)

    model.to_disk("trained_ner_model")

    print("✅ Model trained and saved.")
