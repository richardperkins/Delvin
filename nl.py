import spacy
from datetime import datetime, timedelta
import re

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# Example query
query = "Show truck sales in California for the past two weeks"

# Process the query with SpaCy
doc = nlp(query)

# Print the text (optional)
print("Processed Query:", doc.text)

# Step 1: Identify the verb (action)
verb = None
for token in doc:
    if token.pos_ == "VERB":
        verb = token.text
print("\nVerb (Action):", verb)

# Step 2: Extract noun phrases (category)
nouns = [chunk.text for chunk in doc.noun_chunks]
print("\nNoun Phrases (Category):", nouns)

# Step 3: Extract temporal expression
time_expr = None
for ent in doc.ents:
    if ent.label_ in ("TIME", "DATE"):
        time_expr = ent.text
print("\nTemporal Expression:", time_expr)

# Step 4: Extract location (if available)
location = None
for ent in doc.ents:
    if ent.label_ == "GPE":  # GPE stands for Geopolitical entity (location)
        location = ent.text
print("\nLocation:", location)

# Step 5: Parse the temporal expression
time_delta = None
if time_expr:
    # Improved regex for time-based expressions (e.g., "past two weeks")
    match = re.search(r"(past|last)\s*(\d+|\w+)?\s?(week|month|day|year)s?", time_expr.lower())
    
    if match:
        # Extract number of units and the unit (week/month/day)
        number_of_units = match.group(2) if match.group(2) else '1'  # Default to 1 if no number is given
        unit = match.group(3)

        # Convert textual number to integer if needed
        if number_of_units.isalpha():
            number_of_units = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}.get(number_of_units, 1)
        else:
            number_of_units = int(number_of_units)

        # Calculate the date range based on the number of weeks/months/days
        if unit == "week":
            time_delta = timedelta(weeks=number_of_units)
        elif unit == "day":
            time_delta = timedelta(days=number_of_units)
        elif unit == "month":
            # Approximate the month as 30 days
            time_delta = timedelta(days=30 * number_of_units)

        # Calculate the date range (e.g., 'past two weeks')
        end_date = datetime.today()
        start_date = end_date - time_delta

        print("\nDate Range: From {} to {}".format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))

# Combine the extracted data
extracted_info = {
    "action": verb,
    "category": nouns,
    "location": location,
    "time_frame": time_expr,
    "date_range": {"from": start_date.strftime("%Y-%m-%d"), "to": end_date.strftime("%Y-%m-%d")} if time_delta else None
}

# Output extracted information
print("\nExtracted Information:", extracted_info)
