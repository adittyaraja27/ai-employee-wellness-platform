
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from ingestion.text_ingestion import validate_text
from preprocessing.text_preprocessor import preprocess_text
from sentiment.vader_analyzer import analyze_sentiment
from emotion.confidence import calculate_confidence


MODEL_PATH = "models/bert"


class MoodMentorPipeline:

    def __init__(self, model_path=MODEL_PATH):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)

        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")

        self.model.to(self.device)
        self.model.eval()

    def analyze_emotion(self, text):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits.detach().cpu().numpy()[0]

        return calculate_confidence(logits)

    def analyze(self, text):

        # Validate original input
        if not validate_text(text):
            raise ValueError("Text cannot be empty or invalid")

        # M1 preprocessing
        preprocessed_text = preprocess_text(text)

        if not preprocessed_text:
            raise ValueError("Text became empty after preprocessing")

        # M1 VADER sentiment uses original natural text
        sentiment_result = analyze_sentiment(text)

        # Transformer uses preprocessed M1 text
        emotion_result = self.analyze_emotion(preprocessed_text)

        return {
            "text": text,
            "preprocessed_text": preprocessed_text,
            "sentiment": sentiment_result,
            "emotions": emotion_result
        }


def analyze_text(text):
    pipeline = MoodMentorPipeline()
    return pipeline.analyze(text)


if __name__ == "__main__":

    pipeline = MoodMentorPipeline()

    sample_text = (
        "I am excited about my promotion, "
        "but I am also nervous about the new responsibilities."
    )

    result = pipeline.analyze(sample_text)

    print("\nMood Mentor Analysis")
    print("=" * 50)

    print("\nOriginal Text:")
    print(result["text"])

    print("\nPreprocessed Text:")
    print(result["preprocessed_text"])

    print("\nSentiment:")
    print(result["sentiment"]["sentiment"])

    print("\nSentiment Scores:")
    print(f"Positive: {result['sentiment']['positive']:.4f}")
    print(f"Negative: {result['sentiment']['negative']:.4f}")
    print(f"Neutral: {result['sentiment']['neutral']:.4f}")
    print(f"Compound: {result['sentiment']['compound']:.4f}")

    print("\nDetected Emotions:")

    for emotion in result["emotions"]["detected_emotions"]:
        confidence = result["emotions"]["emotions"][emotion]
        print(f"{emotion}: {confidence:.4f}")

    print("\nPrimary Emotion:")
    print(
        f"{result['emotions']['primary_emotion']} "
        f"({result['emotions']['primary_confidence']:.4f})"
    )
