import pandas as pd

def search_recipes(data, user_input):
    query = user_input.get("query", "").lower()
    filtered_data = data.copy()

    # Search by title/recipe name
    filtered_data = filtered_data[
        filtered_data["title"].str.contains(query, case=False, na=False)
    ]

    # Search by ingredients
    ingredient_columns = [
        col for col in data.columns if col not in ["title", "tags", "calories", "protein", "fat", "sodium"]
    ]
    ingredient_matches = data[ingredient_columns].apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
    filtered_data = pd.concat([filtered_data, data[ingredient_matches]])

    # Search by tags
    tag_columns = [col for col in data.columns if col in ["tags"]]
    for tag_col in tag_columns:
        filtered_data = pd.concat([
            filtered_data,
            data[data[tag_col].astype(str).str.contains(query, case=False, na=False)]
        ])

    # Remove duplicates (if query matches multiple fields)
    filtered_data = filtered_data.drop_duplicates()

    # Return the filtered data
    return filtered_data
