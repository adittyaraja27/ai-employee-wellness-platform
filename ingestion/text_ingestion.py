import pandas as pd
from pathlib import Path


def read_text_input(text):
    return text


def read_txt_file(file_path):
    if Path(file_path).suffix.lower() != ".txt":
        raise ValueError("Only .txt files are supported")

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def read_csv_file(file_path):
    if Path(file_path).suffix.lower() != ".csv":
        raise ValueError("Only .csv files are supported")

    df = pd.read_csv(file_path)

    if "text" not in df.columns:
        raise ValueError("CSV must contain a 'text' column")

    texts = df["text"].dropna().astype(str).tolist()

    texts = [text for text in texts if text.strip()]

    if not texts:
        raise ValueError("CSV contains no valid text")

    return texts


def validate_text(text):
    if text is None:
        return False

    if not isinstance(text, str):
        return False

    if not text.strip():
        return False

    return True