def search_recipes(data, user_input):
    query = user_input.get("query", "").lower()
    filtered_data = data[
        data["title"].str.contains(query, case=False, na=False)
        | data["ingredients"].str.contains(query, case=False, na=False)
    ]
    return filtered_data
