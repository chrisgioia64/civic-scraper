from datetime import datetime, date, timedelta

def to_lowercase(text):
    return text.lower()

# Example usage
input_text = "Hello, World!"
print(input_text.lower())


# Example string
date_string = "11/15/2024"

# Convert string to date
date_object = datetime.strptime(date_string, "%m/%d/%Y").date()
print(date_object)