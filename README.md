
cat > README.md <<'EOF'
# Mood Mentor — AI-Based Employee Wellness Management Platform

An AI-powered employee wellness project developed as part of the **Infosys Springboard Virtual Internship 7.0**.

Mood Mentor analyzes employee-written text to estimate sentiment and emotional indicators, classify emotions, and generate wellness activity recommendations. It combines traditional NLP, transformer models, recommendation techniques, and interactive dashboards.

> **Disclaimer:** This is an educational prototype, not a clinical diagnostic tool. Predictions may be inaccurate and should not be used as the sole basis for employment, medical, or other high-impact decisions.

## Features

- Text ingestion and validation for direct input, TXT, and CSV.
- Text preprocessing with NLTK tokenization, stopword removal, and lemmatization.
- VADER sentiment analysis.
- BERT and DistilBERT emotion classification for joy, sadness, anger, fear, surprise, and disgust.
- Emotion confidence, intensity, and emotional-state analysis.
- Personalized wellness recommendations and recommendation explanations.
- Emotional trend analysis and feedback tracking.
- Flask and Streamlit dashboards.
- Wellness reports and recommendation-interaction CSV export.
- Model evaluation, edge-case testing, and performance benchmarks.

## Architecture

```text
Employee-written text
        |
        v
Input validation and preprocessing
        |
        +----------------------+
        |                      |
        v                      v
VADER sentiment         Transformer emotion
analysis                classification
        |                      |
        +-----------+----------+
                    |
                    v
       Confidence, intensity, and
          emotional-state analysis
                    |
                    v
        Recommendations and trends
                    |
                    v
        Dashboards, history, reports
```

## Technology Stack

- Python 3.12
- PyTorch and Hugging Face Transformers
- NLTK and VADER
- NumPy, pandas, scikit-learn, and Hugging Face Datasets
- Sentence Transformers
- Flask and Streamlit
- pytest

## Project Structure

- `dashboard/` — Flask routes, templates, and styles
- `emotion/` — Emotion labels, confidence, intensity, and emotional state
- `evaluation/` — Model evaluation and ISEAR validation
- `ingestion/` — Text, TXT, and CSV ingestion
- `integration/` — Integrated Mood Mentor pipeline
- `preprocessing/` — Text preprocessing
- `recommendation/` — Recommendations, explanations, and feedback
- `reports/` — Sentiment, wellness, and benchmark reports
- `sentiment/` — VADER analysis
- `training/` — Dataset preparation and model training
- `user/` — User history and profile
- `tests/` — Automated tests
- `benchmarks/` — Pipeline and stress benchmarks
- `streamlit_app.py` — Streamlit dashboard
- `main.py` — Ingestion and preprocessing demonstration
- `requirements.txt` — Python dependencies

## Requirements

- Python 3.12 and Git
- Internet access for installing dependencies and downloading NLTK resources
- The trained BERT checkpoint under `models/bert` for the default pipeline

Model checkpoint directories are excluded from Git. Installing the Python dependencies does not download the trained project checkpoint; obtain the compatible model files separately before running the dashboards.

## Installation on macOS

From the repository root:

```bash
python3.12 -m venv .venv-m2
source .venv-m2/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m nltk.downloader punkt punkt_tab stopwords wordnet vader_lexicon
```

Confirm the default model exists:

```bash
ls models/bert
```

The pipeline uses Apple's MPS device when PyTorch reports it is available; otherwise, it uses the CPU.

## Run the Dashboards

### Streamlit

```bash
streamlit run streamlit_app.py
```

Open the local URL printed by Streamlit.

### Flask

```bash
python -m dashboard.app
```

Open `http://127.0.0.1:5001`.

The Flask development server is intended for local development, not direct production deployment.

### Ingestion and preprocessing demonstration

```bash
python main.py
```

## Tests

Run the complete test suite:

```bash
python -m pytest
```

Run dashboard route tests only:

```bash
python -m pytest tests/test_dashboard_routes.py -q
```

Tests that load the real transformer pipeline require the model checkpoint and its dependencies.

## Evaluation and Benchmarks

Available scripts include:

```bash
python evaluation/evaluate_bert.py
python evaluation/evaluate_distilbert.py
python evaluation/isear_validation.py
python benchmarks/benchmark_pipeline.py
python benchmarks/stress_test_pipeline.py
python benchmarks/concurrent_stress_test.py
```

These scripts may require trained checkpoints, datasets, and additional computation. Review each script before running it. Stored benchmark results describe the recorded environment and do not guarantee performance on other machines.

Previously recorded evaluation results:

| Model | Accuracy | Precision | Recall | Macro F1 |
|---|---:|---:|---:|---:|
| BERT | 0.7500 | 0.7824 | 0.6348 | 0.6951 |
| DistilBERT | 0.7437 | 0.7985 | 0.5998 | 0.6714 |

These results reflect a recorded evaluation run, not guaranteed performance on real workplace text.

## Privacy and Limitations

- Mood entries may contain sensitive personal information. Use synthetic or non-sensitive text for demonstrations.
- Emotional history and recommendation feedback are stored in application memory and may be lost when the process restarts.
- Wellness report exports are designed to exclude raw mood text.
- Emotion classification can misinterpret context, sarcasm, cultural differences, and ambiguous language.
- Before real deployment, add appropriate authentication, authorization, storage controls, data-retention policies, and consent mechanisms.

## Internship Context

Developed for the **Infosys Springboard Virtual Internship 7.0**, this project combines NLP preprocessing, sentiment analysis, transformer-based emotion classification, recommendations, reporting, and interactive dashboards.

## License

See the repository's `MIT License` file.
EOF
