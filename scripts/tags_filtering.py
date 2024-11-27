def filter_recipes_by_tags(data, tags):
    for tag, value in tags.items():
        if value:
            data = data[data[tag] == value]
    return data
