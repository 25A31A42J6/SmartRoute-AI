# SmartRoute AI — Technical Paper

## Abstract
Customer-support systems receive large volumes of natural-language requests that must be classified and routed to suitable service functions. SmartRoute AI implements a lightweight multi-class NLP pipeline using TF-IDF text representation and Logistic Regression. A Flask backend exposes the trained pipeline to an HTML/CSS/JavaScript interface. The application also adds a confidence-aware routing layer, service-queue mapping, routing history, and browser-based analytics.

## 1. Problem Statement
The capstone task is Customer Query Routing Classification: classify incoming support queries into predefined service categories so that requests can be routed to an appropriate service queue.

## 2. Dataset
The project uses BANKING77 for the final experiment. The final local run used 10,003 training examples, 3,080 official test examples, and 77 intent classes. The dataset is a customer-service intent classification benchmark and should be cited with its original source and license in the submitted work.

## 3. Methodology
1. Load the training and official test CSV files.
2. Validate columns and remove invalid/duplicate records where applicable.
3. Represent customer messages with TF-IDF features.
4. Train a multi-class Logistic Regression classifier.
5. Evaluate on the official test split.
6. Serialize the complete preprocessing/model pipeline.
7. Serve predictions through Flask.
8. Apply a transparent confidence-based routing policy.

## 4. EDA Findings
The final EDA run reported:
- Training shape: 10,003 × 2.
- Test shape: 3,080 × 2.
- Columns: `text`, `category`.
- Missing values: 0 in both fields.
- Duplicate rows: 0 in the training and test splits.
- Exact train/test text overlap: 0.
- Number of classes: 77.
- Mean query length: approximately 11.95 words and 59.48 characters in the training data.

The class distribution is reasonably spread across the 77 intents, although individual intent counts differ.

## 5. Evaluation
The final local official-test run produced:

| Metric | Result |
|---|---:|
| Accuracy | **87.24%** |
| Weighted Precision | **88.02%** |
| Weighted Recall | **87.24%** |
| Weighted F1-score | **87.26%** |

The classification report and confusion matrix generated during the local run should be retained in the submission folder if available.

## 6. Prototype
The web interface provides:
- Customer query input with character counter.
- Predicted service intent.
- Model confidence indicator.
- Top three predicted intents.
- Confidence-aware routing decision.
- Recommended service queue.
- Recent routing history.
- Decision distribution analytics.
- Service-queue distribution analytics.
- Average confidence across analyzed queries.

Routing history is stored in the browser using `localStorage` for demonstration purposes; it is not a production database.

## 7. Limitations
TF-IDF + Logistic Regression is a classical baseline and can struggle when two intents use highly similar language or when a query is phrased very differently from the training distribution. The routing thresholds are application-level rules and should not be interpreted as calibrated probability guarantees. Service-queue mappings are project-specific and should be validated before real operational use.

## 8. Future Work
Potential extensions include probability calibration, richer metadata, human-in-the-loop feedback, multilingual support, monitoring of drift, and comparison with transformer-based models after the classical baseline is established.

## 9. Conclusion
SmartRoute AI demonstrates an end-to-end customer-query routing prototype using conventional NLP and machine learning. The final local experiment achieved 87.24% accuracy on the official BANKING77 test split, while the frontend demonstrates how predictions can be converted into transparent operational routing decisions.
