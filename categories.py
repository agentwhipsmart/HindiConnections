import random

all_hindi_sets = [
    {
        "Yellow": ["word1", "word2", "word3", "word4"],
        "Green": ["word5", "word6", "word7", "word8"],
        "Blue": ["word9", "word10", "word11", "word12"],
        "Purple": ["word13", "word14", "word15", "word16"]
    },
    # Add more sets here...
]


# Function to get categories ordered by difficulty
def get_ordered_categories(category_set):
    categories = list(category_set.keys())
    return {
        categories[0]: category_set[categories[0]],  # Yellow (Easiest)
        categories[1]: category_set[categories[1]],  # Green (Medium-Easy)
        categories[2]: category_set[categories[2]],  # Blue (Difficult)
        categories[3]: category_set[categories[3]]   # Purple (Most Difficult)
    }

# Randomly select a set and order it by difficulty
selected_set = random.choice(all_hindi_sets)
all_categories = get_ordered_categories(selected_set)

# Example usage (replace with your actual game logic)
print(all_categories)