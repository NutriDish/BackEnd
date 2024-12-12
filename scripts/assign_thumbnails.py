import csv
import random
from firebase_admin import firestore, initialize_app, credentials

# Initialize Firebase App
SERVICE_ACCOUNT_KEY_PATH = "config/serviceAccountKey.json"
cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
initialize_app(cred)

db = firestore.client()

# Load image paths and URLs from CSV
def load_image_data(csv_file):
    """
    Reads the image_path_url.csv and returns a list of image data.
    :param csv_file: Path to the CSV file.
    :return: List of dictionaries with 'path' and 'url'.
    """
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        return [{"path": row["path"], "url": row["url"]} for row in reader]

# Assign a random image URL to a recipe
def get_random_image_url(images):
    """
    Selects a random image URL from the list of images.
    :param images: List of image dictionaries.
    :return: Random image URL.
    """
    return random.choice(images)["url"]

# Retrieve recipes from Firestore and assign thumbnails
def assign_thumbnails_to_firestore_recipes(collection_name, images):
    """
    Retrieves recipes from Firestore, assigns random thumbnails, and updates Firestore.
    :param collection_name: Name of the Firestore collection.
    :param images: List of image dictionaries.
    """
    recipes_ref = db.collection(collection_name)
    recipes = recipes_ref.stream()

    for recipe_doc in recipes:
        recipe_data = recipe_doc.to_dict()
        recipe_data["image_url"] = get_random_image_url(images)  # Add thumbnail

        # Update Firestore with the new image URL
        recipes_ref.document(recipe_doc.id).set(recipe_data)
        print(f"Updated recipe: {recipe_doc.id} with image_url: {recipe_data['image_url']}")

# Example Usage
if __name__ == "__main__":
    # Load image data from CSV
    image_data = load_image_data("data/image_path_url.csv")

    # Assign thumbnails to recipes in Firestore
    assign_thumbnails_to_firestore_recipes("recipes", image_data)
