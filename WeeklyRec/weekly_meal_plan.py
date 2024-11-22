
    Generate a weekly meal plan with cooldown and fallback handling.

    Parameters:
    - data (DataFrame): Filtered recipe dataset.
    - user_input (dict): User preferences and tags.
    - cooldown_tracker (dict, optional): Tracks recipes on cooldown. Defaults to None.
    - cooldown_weeks (int): Number of weeks a recipe remains on cooldown.

    Returns:
    - dict: Weekly meal plan with recipes per day and meal type.
    - dict: Updated cooldown tracker.
    