import re

# Test string
test_string = "666fe8f4106dd16f8e325c58--B-Ge-i-1-653"

# Regex pattern per matchare il valore tra -B- e -i-
pattern = r"(\w*)--(\w*)-(\w*)-(.*)"

match = re.search(pattern, test_string)
if match:
    extracted_value = match.group(3)
    print(extracted_value)  # Output: Ge
else:
    print("Pattern non trovato")
