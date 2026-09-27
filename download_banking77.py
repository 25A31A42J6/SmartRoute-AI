
"""
Download the official BANKING77 CSV files.

Run:
    python download_banking77.py

This requires internet access on the machine running the project.
The official dataset contains 13,083 queries across 77 intents.
"""
import os
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

URLS = {
    "banking77_train.csv":
        "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/train.csv",
    "banking77_test.csv":
        "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/test.csv",
}

for filename, url in URLS.items():
    path = os.path.join(DATA, filename)
    print(f"Downloading {filename}...")
    urllib.request.urlretrieve(url, path)
    print(f"Saved: {path}")

print("\nDownload complete.")
print("Then train with:")
print("python train_model.py --data data/banking77_train.csv")