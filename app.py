from flask import Flask, render_template, request, jsonify
import os
import pickle


# ============================================================
# APP CONFIGURATION
# ============================================================

app = Flask(__name__)

ROOT = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    ROOT,
    "model",
    "smartroute_pipeline.pkl"
)


# ============================================================
# LOAD MODEL
# ============================================================

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    MODEL_STATUS = "online"

except Exception as error:
    model = None
    MODEL_STATUS = "error"

    print("ERROR: Could not load SmartRoute model.")
    print(error)


# ============================================================
# LABEL FORMATTING
# ============================================================

def pretty_label(label):
    """
    Convert BANKING77 labels such as:

        card_payment_fee_charged

    into:

        Card Payment Fee Charged
    """

    return str(label).replace("_", " ").title()


# ============================================================
# CONFIDENCE-AWARE ROUTING
# ============================================================

def route_by_confidence(confidence):
    """
    Confidence-aware application routing policy.

    confidence is expected as a decimal between 0 and 1.

    >= 0.80  -> Auto Route
    >= 0.60  -> Route + Review
    <  0.60  -> Human Review
    """

    confidence = float(confidence)

    if confidence >= 0.80:

        return {
            "level": "high",
            "label": "Auto Route",
            "detail": "High-confidence classification"
        }

    elif confidence >= 0.60:

        return {
            "level": "medium",
            "label": "Route + Review",
            "detail": "Classification is usable, but review is recommended"
        }

    else:

        return {
            "level": "low",
            "label": "Human Review",
            "detail": "Low-confidence classification"
        }


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health")
def health():

    return jsonify({
        "status": MODEL_STATUS,
        "model": "SmartRoute AI",
        "dataset": "BANKING77"
    })


# ============================================================
# PREDICTION API
# ============================================================

@app.route("/api/predict", methods=["POST"])
def predict():

    # --------------------------------------------------------
    # Check model
    # --------------------------------------------------------

    if model is None:

        return jsonify({
            "success": False,
            "error": "SmartRoute model could not be loaded."
        }), 500


    # --------------------------------------------------------
    # Read request
    # --------------------------------------------------------

    data = request.get_json(silent=True) or {}

    text = str(
        data.get("text", "")
    ).strip()


    # --------------------------------------------------------
    # Validate query
    # --------------------------------------------------------

    if not text:

        return jsonify({
            "success": False,
            "error": "Please enter a customer query."
        }), 400


    if len(text) > 1000:

        return jsonify({
            "success": False,
            "error": "Query must be 1000 characters or less."
        }), 400


    try:

        # ----------------------------------------------------
        # Get class probabilities
        # ----------------------------------------------------

        probabilities = model.predict_proba([text])[0]

        classes = model.classes_


        # ----------------------------------------------------
        # Rank predictions
        # ----------------------------------------------------

        ranked = sorted(
            zip(classes, probabilities),
            key=lambda item: item[1],
            reverse=True
        )[:3]


        # ----------------------------------------------------
        # Best prediction
        # ----------------------------------------------------

        prediction, top_probability = ranked[0]

        confidence = float(top_probability)


        # ----------------------------------------------------
        # Routing decision
        # ----------------------------------------------------

        routing = route_by_confidence(
            confidence
        )


        # ----------------------------------------------------
        # Top 3 predictions
        # ----------------------------------------------------

        top_predictions = [

            {
                "category": str(label),

                "display_category":
                    pretty_label(label),

                "confidence":
                    round(float(probability) * 100, 2)
            }

            for label, probability in ranked
        ]


        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "query": text,

            "category":
                str(prediction),

            "display_category":
                pretty_label(prediction),

            "confidence":
                round(confidence * 100, 2),

            "routing":
                routing,

            "top_predictions":
                top_predictions
        })


    except Exception as error:

        print("Prediction error:")
        print(error)

        return jsonify({
            "success": False,
            "error": "Prediction failed. Please check the model and server logs."
        }), 500


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )