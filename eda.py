import os
import re
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "eda_outputs")

os.makedirs(OUT, exist_ok=True)

train = pd.read_csv(os.path.join(DATA, "banking77_train.csv"))
test = pd.read_csv(os.path.join(DATA, "banking77_test.csv"))

print("=" * 60)
print("SMARTROUTE AI — BANKING77 EDA")
print("=" * 60)

print("\nTrain shape:", train.shape)
print("Test shape :", test.shape)
print("Columns:", train.columns.tolist())
print("Number of classes:", train["category"].nunique())

print("\n--- Missing Values ---")
print(train.isna().sum())

print("\n--- Duplicate Rows ---")
print("Train:", train.duplicated().sum())
print("Test :", test.duplicated().sum())

train["word_count"] = train["text"].astype(str).str.split().str.len()
train["char_count"] = train["text"].astype(str).str.len()

print("\n--- Query Length Statistics ---")
print(train[["word_count", "char_count"]].describe().round(2))

# Class distribution
counts = train["category"].value_counts()

print("\n--- CLASS DISTRIBUTION ---")
print(counts.to_string())

plt.figure(figsize=(12, 18))
counts.sort_values().plot(kind="barh")
plt.title("BANKING77 Training Set — Intent Distribution")
plt.xlabel("Number of Queries")
plt.ylabel("Intent")
plt.tight_layout()
plt.savefig(
    os.path.join(OUT, "class_distribution.png"),
    dpi=180
)
plt.close()

# Word count distribution
plt.figure(figsize=(10, 5))
plt.hist(train["word_count"], bins=35)
plt.title("Query Word Count Distribution")
plt.xlabel("Words per Query")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(
    os.path.join(OUT, "word_count_distribution.png"),
    dpi=180
)
plt.close()

# Character length distribution
plt.figure(figsize=(10, 5))
plt.hist(train["char_count"], bins=40)
plt.title("Query Character Length Distribution")
plt.xlabel("Characters per Query")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(
    os.path.join(OUT, "character_length_distribution.png"),
    dpi=180
)
plt.close()

# Top words
tokens = []

for text in train["text"].astype(str):
    tokens.extend(
        re.findall(r"[a-zA-Z]+", text.lower())
    )

stop_words = {
    "the", "a", "an", "and", "or", "to", "of",
    "is", "i", "my", "it", "in", "for", "on",
    "me", "this", "that", "do", "does", "can",
    "how", "what", "why", "was", "be", "have",
    "has", "with", "are", "am", "please",
    "there", "you"
}

word_counts = Counter(
    word
    for word in tokens
    if word not in stop_words and len(word) > 2
)

top_words = word_counts.most_common(25)

plt.figure(figsize=(10, 7))

words = [x[0] for x in top_words][::-1]
values = [x[1] for x in top_words][::-1]

plt.barh(words, values)

plt.title("Top 25 Words in BANKING77")
plt.xlabel("Frequency")

plt.tight_layout()

plt.savefig(
    os.path.join(OUT, "top_words.png"),
    dpi=180
)

plt.close()

# Leakage check
train_texts = set(train["text"].astype(str))
test_texts = set(test["text"].astype(str))

overlap = train_texts.intersection(test_texts)

print("\n--- DATA LEAKAGE CHECK ---")
print("Exact train/test text overlap:", len(overlap))

# Save summary
summary = f"""
SMARTROUTE AI — BANKING77 EDA SUMMARY

Train shape: {train.shape}
Test shape: {test.shape}

Columns:
{train.columns.tolist()}

Number of classes:
{train["category"].nunique()}

Missing values:
{train.isna().to_string()}

Duplicate rows:
Train: {train.duplicated().sum()}
Test: {test.duplicated().sum()}

Query length statistics:
{train[["word_count", "char_count"]].describe().round(2).to_string()}

Exact train/test text overlap:
{len(overlap)}

Largest classes:
{counts.head(10).to_string()}

Smallest classes:
{counts.tail(10).to_string()}

Top words:
{chr(10).join(f"{w}: {c}" for w, c in top_words)}
"""

with open(
    os.path.join(OUT, "eda_summary.txt"),
    "w",
    encoding="utf-8"
) as f:
    f.write(summary)

print("\n" + "=" * 60)
print("EDA COMPLETE")
print("=" * 60)

print("\nGenerated files:")
print("  eda_outputs/class_distribution.png")
print("  eda_outputs/word_count_distribution.png")
print("  eda_outputs/character_length_distribution.png")
print("  eda_outputs/top_words.png")
print("  eda_outputs/eda_summary.txt")