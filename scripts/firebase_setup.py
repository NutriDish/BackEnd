import csv
import random

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

# Example Usage
if __name__ == "__main__":
    images = load_image_data("data/image_path_url.csv")  # Load image data
    random_image_url = get_random_image_url(images)  # Get a random image URL
    print(f"Random Image URL: {random_image_url}")
