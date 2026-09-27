import os
import json
import pickle
import argparse

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)


ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(ROOT, "model")

DEFAULT_TRAIN = os.path.join(
    ROOT, "data", "banking77_train.csv"
)

DEFAULT_TEST = os.path.join(
    ROOT, "data", "banking77_test.csv"
)


def load_data(path):
    df = pd.read_csv(path)

    # BANKING77 uses "category"
    if "category" in df.columns:
        df = df.rename(columns={"category": "label"})

    df = (
        df
        .dropna(subset=["text", "label"])
        .drop_duplicates()
    )

    return df


def main(train_path, test_path):

    print("=" * 65)
    print("SMARTROUTE AI — FINAL BANKING77 MODEL")
    print("=" * 65)

    # -----------------------------
    # Load datasets
    # -----------------------------

    train_df = load_data(train_path)
    test_df = load_data(test_path)

    print("\nTraining samples:", len(train_df))
    print("Testing samples :", len(test_df))
    print("Number of classes:", train_df["label"].nunique())

    X_train = train_df["text"].astype(str)
    y_train = train_df["label"].astype(str)

    X_test = test_df["text"].astype(str)
    y_test = test_df["label"].astype(str)

    # -----------------------------
    # Build ML pipeline
    # -----------------------------

    pipeline = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                strip_accents="unicode",
                ngram_range=(1, 2),
                sublinear_tf=True,
                min_df=1
            )
        ),

        (
            "classifier",
            LogisticRegression(
                max_iter=3000,
                class_weight="balanced",
                random_state=42
            )
        )
    ])

    print("\nTraining TF-IDF + Logistic Regression...")

    pipeline.fit(X_train, y_train)

    print("Training complete.")

    # -----------------------------
    # Prediction
    # -----------------------------

    print("\nEvaluating on official test set...")

    predictions = pipeline.predict(X_test)

    # -----------------------------
    # Metrics
    # -----------------------------

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    print("\n" + "=" * 65)
    print("FINAL TEST RESULTS")
    print("=" * 65)

    print(f"\nAccuracy          : {accuracy * 100:.2f}%")
    print(f"Weighted Precision: {precision * 100:.2f}%")
    print(f"Weighted Recall   : {recall * 100:.2f}%")
    print(f"Weighted F1-score : {f1 * 100:.2f}%")

    # -----------------------------
    # Classification report
    # -----------------------------

    report = classification_report(
        y_test,
        predictions,
        zero_division=0
    )

    print("\nCLASSIFICATION REPORT")
    print("=" * 65)
    print(report)

    # -----------------------------
    # Confusion matrix
    # -----------------------------

    labels = sorted(y_test.unique())

    cm = confusion_matrix(
        y_test,
        predictions,
        labels=labels
    )

    plt.figure(figsize=(22, 20))

    plt.imshow(
        cm,
        interpolation="nearest"
    )

    plt.title(
        "SmartRoute AI — BANKING77 Confusion Matrix"
    )

    plt.xlabel("Predicted Category")
    plt.ylabel("Actual Category")

    plt.colorbar()

    plt.xticks(
        range(len(labels)),
        labels,
        rotation=90,
        fontsize=6
    )

    plt.yticks(
        range(len(labels)),
        labels,
        fontsize=6
    )

    plt.tight_layout()

    confusion_path = os.path.join(
        MODEL_DIR,
        "confusion_matrix.png"
    )

    plt.savefig(
        confusion_path,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    # -----------------------------
    # Save model
    # -----------------------------

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    model_path = os.path.join(
        MODEL_DIR,
        "smartroute_pipeline.pkl"
    )

    with open(
        model_path,
        "wb"
    ) as file:

        pickle.dump(
            pipeline,
            file
        )

    # -----------------------------
    # Save metrics
    # -----------------------------

    metrics = {
        "dataset": "BANKING77",
        "training_samples": len(train_df),
        "test_samples": len(test_df),
        "classes": int(train_df["label"].nunique()),
        "accuracy": round(float(accuracy), 6),
        "weighted_precision": round(float(precision), 6),
        "weighted_recall": round(float(recall), 6),
        "weighted_f1": round(float(f1), 6),
        "model": "TF-IDF + Logistic Regression",
        "ngram_range": "(1,2)",
        "random_state": 42
    }

    metrics_path = os.path.join(
        MODEL_DIR,
        "metrics.json"
    )

    with open(
        metrics_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4
        )

    # -----------------------------
    # Save text report
    # -----------------------------

    report_path = os.path.join(
        MODEL_DIR,
        "classification_report.txt"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "SMARTROUTE AI — BANKING77 FINAL EVALUATION\n"
        )

        file.write("=" * 65 + "\n\n")

        file.write(
            f"Training samples: {len(train_df)}\n"
        )

        file.write(
            f"Test samples: {len(test_df)}\n"
        )

        file.write(
            f"Classes: {train_df['label'].nunique()}\n\n"
        )

        file.write(
            f"Accuracy: {accuracy * 100:.2f}%\n"
        )

        file.write(
            f"Weighted Precision: {precision * 100:.2f}%\n"
        )

        file.write(
            f"Weighted Recall: {recall * 100:.2f}%\n"
        )

        file.write(
            f"Weighted F1: {f1 * 100:.2f}%\n\n"
        )

        file.write(
            "Classification Report\n"
        )

        file.write("=" * 65 + "\n")

        file.write(report)

    print("\n" + "=" * 65)
    print("FINAL MODEL SAVED")
    print("=" * 65)

    print("\nModel:")
    print("model/smartroute_pipeline.pkl")

    print("\nMetrics:")
    print("model/metrics.json")

    print("\nClassification report:")
    print("model/classification_report.txt")

    print("\nConfusion matrix:")
    print("model/confusion_matrix.png")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--train",
        default=DEFAULT_TRAIN
    )

    parser.add_argument(
        "--test",
        default=DEFAULT_TEST
    )

    args = parser.parse_args()

    main(
        args.train,
        args.test
    )