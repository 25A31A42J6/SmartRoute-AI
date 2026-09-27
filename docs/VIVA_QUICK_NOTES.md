# SmartRoute AI — Viva Quick Notes

**Problem:** Customer Query Routing Classification.

**Why NLP?** Customer queries are unstructured text, so the system converts language into numerical TF-IDF features.

**Why TF-IDF?** It is lightweight, interpretable, fast, and appropriate for a classical NLP baseline.

**Why Logistic Regression?** It is a strong, efficient linear classifier for sparse TF-IDF features and naturally supports multi-class classification.

**Dataset:** BANKING77 — 77 customer-service intents; final run used 10,003 training examples and 3,080 official test examples.

**Final accuracy:** 87.24% on the official test split.

**What does confidence mean?** The displayed value is the classifier's top predicted probability/score from `predict_proba`; the app then applies project-defined routing thresholds.

**Why human review?** Low-confidence predictions should not be treated as automatic operational decisions.

**Frontend:** HTML5, CSS3 and JavaScript.

**Backend:** Flask.

**Deployment:** Local Flask prototype.

**Main limitation:** Similar intents can have overlapping language, and the model is domain-specific.
