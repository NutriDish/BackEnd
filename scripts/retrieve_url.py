import firebase_admin
from firebase_admin import credentials, storage
import csv
from pathlib import Path

# Initialize Firebase Admin SDK
path = Path(__file__).resolve().parent.parent / "NutriDish" / "config" / "serviceAccountKey.json"
cred = credentials.Certificate(path)  # Replace with your service account key
firebase_admin.initialize_app(cred, {"storageBucket": "orbital-bee-442114-t3.firebasestorage.app"})  # Replace with your project ID

# Reference to the storage bucket
bucket = storage.bucket()

def list_files_in_filter_recipe_folder():
    """
    List all files in the 'filter_recipe' folder in Firebase Storage and generate their URLs.
    """
    blobs = bucket.list_blobs(prefix="filter_recipe/")  # List files only in the filter_recipe folder
    file_list = []

    for blob in blobs:
        # Get file path and public URL
        file_path = blob.name
        file_url = blob.generate_signed_url(expiration=3600)  # URL valid for 1 hour
        file_list.append({"image_path": file_path, "image_url": file_url})

    # Save results to a CSV file
    with open("image_path_url.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["image_path", "image_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(file_list)

    print(f"File listing completed. Total files: {len(file_list)}. Saved to 'filter_recipe_files.csv'.")

# Run the function
list_files_in_filter_recipe_folder()
