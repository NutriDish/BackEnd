from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from scripts.model_utils import predict_ingredient

db = firestore.client()
image_classification_blueprint = Blueprint("image_classification", __name__)

@image_classification_blueprint.route("/", methods=["POST"])
def classify_image():
    """
    Classify the uploaded image and predict the ingredient, then search for recipes.
    """
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image_file = request.files["image"]
        image_bytes = image_file.read()

        # Predict ingredient
        predicted_label, confidence = predict_ingredient(image_bytes)

        # Search for recipes containing the predicted ingredient
        recipes_ref = db.collection("recipes").where(f"has_{predicted_label.lower()}", "==", True)
        recipes = [doc.to_dict() for doc in recipes_ref.stream()]

        # Return predictions and recipe search results
        return jsonify({
            "ingredient": predicted_label,
            "confidence": float(confidence),
            "recipes": recipes  # Include recipes in the response
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
