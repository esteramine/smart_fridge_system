from datetime import datetime 
from datetime import timedelta 
from datetime import date 

expiration_day_info = {
    # fresh produce
    "leafy_greens": "3 days",
    "broccoli_and_cauliflower": "1 week",
    "root_vegetables": "2 weeks",
    "berries": "3 days",
    "citrus_fruits": "2 weeks",
    "bell_peppers": "1 weeks",
    "zucchini_and_summer_squash": "1 week",
    "cucumbers": "1 week",
    "green_beans": "1 week",
    "asparagus": "3 days",
    "mushrooms": "4 days",
    "cabbage": "1 weeks",
    "celery": "1 weeks",
    "tomatoes": "3 days",  # (best stored at room temperature until fully ripe)
    # fruits
    "apples": "4 weeks",
    "bananas": "2 days",  # (best stored at room temperature; refrigeration can slow ripening)
    "grapes": "1 weeks",
    "whole_pineapple": "3 days",
    "cut_pineapple": "2 days",
    "whole_melons": "1 week",  # (e.g., cantaloupe, honeydew)
    "cut_melons": "3 days",
    "peaches_plums_and_nectarines": "3 days",
    "pears": "1 weeks",
    "kiwifruit": "1 weeks",
    "avocados": "3 days",  # (best stored at room temperature until ripe, then refrigerate)
    # diary
    "milk": "5 days",
    "soft_cheese": "1 weeks",
    "hard_cheese": "3 weeks",
    "yogurt": "1 weeks",
    # meat and poultry
    "raw_chicken": "1 days",
    "raw_beef_pork_lamb": "3 days",
    "cooked_meat_and_poultry": "3 days",
    "deli_meats": "3 days",
    # seafood
    "fresh_fish": "1 days",
    "shellfish": "1 days", # (e.g., shrimp, clams)
    "smoked_fish": "1 weeks",
    # eggs
    "whole_eggs": "3 weeks",
    "hard_boiled_eggs": "1 week",
    # bread and baked goods
    "bread": "3 days",
    "baked_goods": "1 week",
    # leftovers
    "cooked_rice_and_pasta": "3 days",
    "soups_and_stews": "3 days",
    # pantry items
    "canned_goods_unopened": "1 years",
    "nuts": "4 months",
    "others": "4 days"
}

def __convert_to_days(expiry_string):
    word = expiry_string.split(" ")
    multi = 1
    if "week" in word[1]:
        multi = 7
    elif "month" in word[1]:
        multi = 30
    elif "year" in word[1]:
        multi = 365
    return int(word[0]) * multi 


def get_expiration_date(category):
    now = date.today()
    if category not in expiration_day_info:
        category = "others"
    expiry_days = __convert_to_days(expiration_day_info[category])
    return str(now + timedelta(days=expiry_days))

'''
"leafy_greens", "broccoli_and_cauliflower", "root_vegetables", "berries", "citrus_fruits", "milk", "soft_cheese", "hard_cheese", "yogurt",
"raw_chicken", "raw_beef_pork_lamb", "cooked_meat_and_poultry", "deli_meats",
"fresh_fish", "shellfish", "smoked_fish", "whole_eggs", "hard_boiled_eggs",
"bread", "baked_goods", "cooked_rice_and_pasta", "soups_and_stews",
"canned_goods_unopened", "nuts", "bell_peppers", "zucchini_and_summer_squash", "cucumbers", "green_beans",
"asparagus", "mushrooms", "cabbage", "celery", "tomatoes", "apples",
"bananas", "grapes", "whole_pineapple", "cut_pineapple", "whole_melons", "cut_melons", "peaches_plums_and_nectarines",
"pears", "kiwifruit", "avocados", "others"
'''

# # fresh produce
# "leafy_greens": "3-5 days",
# "broccoli_and_cauliflower": "1 week",
# "root_vegetables": "2-4 weeks",
# "berries": "3-7 days",
# "citrus_fruits": "2-3 weeks",
# "bell_peppers": "1-2 weeks",
# "zucchini_and_summer_squash": "1 week",
# "cucumbers": "1 week",
# "green_beans": "1 week",
# "asparagus": "3-5 days",
# "mushrooms": "4-7 days",
# "cabbage": "1-2 weeks",
# "celery": "1-2 weeks",
# "tomatoes": "3-5 days",  # (best stored at room temperature until fully ripe)
# # fruits
# "apples": "4-6 weeks",
# "bananas": "2-5 days",  # (best stored at room temperature; refrigeration can slow ripening)
# "grapes": "1-2 weeks",
# "pineapple": "3-5 days (whole), 2-3 days (cut)",
# "melons": "1 week (whole), 3-4 days (cut)",  # (e.g., cantaloupe, honeydew)
# "peaches_plums_and_nectarines": "3-5 days",
# "pears": "1-2 weeks",
# "kiwifruit": "1-2 weeks",
# "avocados": "3-4 days",  # (best stored at room temperature until ripe, then refrigerate)
# # diary
# "milk": "5-7 days",
# "soft_cheese": "1-2 weeks",
# "hard_cheese": "3-4 weeks",
# "yogurt": "1-2 weeks",
# # meat and poultry
# "raw_chicken": "1-2 days",
# "raw_beef_pork_lamb": "3-5 days",
# "cooked_meat_and_poultry": "3-4 days",
# "deli_meats": "3-5 days",
# # seafood
# "fresh_fish": "1-2 days",
# "shellfish": "1-2 days", # (e.g., shrimp, clams)
# "smoked_fish": "1-2 weeks",
# # eggs
# "whole_eggs": "3-5 weeks",
# "hard_boiled_eggs": "1 week",
# # bread and baked goods
# "bread": "3-7 days",
# "baked_goods": "1 week",
# # leftovers
# "cooked_rice_and_pasta": "3-5 days",
# "soups_and_stews": "3-4 days",
# # pantry items
# "canned_goods_unopened": "1-2 years",
# "nuts": "4-6 months",
# "others": "4 days"