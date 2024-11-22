
    Save recipe dataset to an SQLite database.

    Parameters:
    - data (DataFrame): Recipe dataset.
    - db_path (str): Path to SQLite database file.
    - table_name (str): Table name for storing recipes.

    Returns:
    - None
    

    Save weekly meal plan to a JSON file.

    Parameters:
    - data (dict): Weekly meal plan or other structured data.
    - json_path (str): Path to save the JSON file.

    Returns:
    - None
    

    Load recipe dataset from an SQLite database.

    Parameters:
    - db_path (str): Path to SQLite database file.
    - table_name (str): Table name for loading recipes.

    Returns:
    - DataFrame: Loaded recipe dataset.
    