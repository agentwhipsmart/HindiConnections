
import random

all_hindi_sets = [
    {
        "सरल शब्द": ["माँ", "पिता", "बेटा", "बेटी"],  # Yellow - Family (Easiest)
        "फल और सब्जियां": ["आम", "केला", "गाजर", "मटर"],  # Green - Fruits and Vegetables
        "त्योहार": ["दिवाली", "होली", "दशहरा", "रक्षाबंधन"],  # Blue - Festivals
        "वैज्ञानिक शब्द": ["परमाणु", "अभिक्रिया", "प्रतिबिंब", "गुरुत्वाकर्षण"]  # Purple - Scientific terms
    },
    {
        "रंग": ["लाल", "नीला", "पीला", "हरा"],  # Yellow - Colors
        "जानवर": ["शेर", "हाथी", "बाघ", "गाय"],  # Green - Animals
        "व्यवसाय": ["वकील", "डॉक्टर", "इंजीनियर", "वैज्ञानिक"],  # Blue - Professions
        "दार्शनिक शब्द": ["आत्मा", "कर्म", "मोक्ष", "धर्म"]  # Purple - Philosophical terms
    }
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
