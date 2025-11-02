import inflect
import re
from word2number import w2n

# Create an instance of the inflect engine
p = inflect.engine()

# Define a mapping for words representing numbers 0-9
word_to_num = {p.number_to_words(i): str(i) for i in range(10)}

# Define sets of common measurement and time units
measurement_units = {"mg", "cm", "ml", "kg", "m", "km", "L", "g", "mm", "in", "ft", "%"}
time_units = {"second", "seconds", "minute", "minutes", "hour", "hours", "day", "days", "month", "months", "year", "years", "decade", "decades"}
all_units = measurement_units.union(time_units)

# Define a dictionary to map currency names to their symbols
currency_mapping = {
    "dollar": "$", "dollars": "$",
    "euro": "€", "euros": "€",
    "pound": "£", "pounds": "£",
    "yen": "¥", "yenes": "¥",
    "rupee": "₹", "rupees": "₹"
}

# Regex patterns for detecting currency and unit patterns
currency_pattern = r"(\d+(\.\d{1,2})?)\s*(\$|€|£|¥|₹)"  # Matches amounts like "5.50 $", "10€"
unit_pattern = r"(\d+|\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one|twenty-two|twenty-three|twenty-four|twenty-five|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion|trillion)\b)\s*(mg|cm|ml|kg|m|km|L|g|mm|in|ft|%|second|seconds|minute|minutes|hour|hours|day|days|month|months|year|years|decade|decades)"

def convert_word_to_number(word):
    """ Convert word-number (10 and above) to numeral using w2n or custom logic for small numbers """
    try:
        # Try to convert using the word2number library for both space-separated and hyphenated numbers
        return str(w2n.word_to_num(word))
    except ValueError:
        pass
    
    # Handle small numbers (0-9) manually using a dictionary
    if word in word_to_num:
        return word_to_num[word]
    
    # If no conversion is possible, return the word as-is
    return word

def process_text(input_text):
    # First, use regex to replace currency and unit patterns
    input_text = re.sub(currency_pattern, lambda m: f"{m.group(3)}{m.group(1)}", input_text)  # Currency handling
    input_text = re.sub(unit_pattern, lambda m: f"{m.group(1)} {m.group(2)}", input_text)  # Units handling

    words = input_text.split()
    processed_words = []

    i = 0
    while i < len(words):
        word = words[i]
        lower_word = word.lower().strip(",.!?")

        # Handle large numbers (e.g., "million", "billion", etc.)
        if lower_word in ["million", "billion", "trillion"]:
            if i > 0:
                # Combine the number and the large number word into one string
                combined_number = f"{words[i-1]} {lower_word}"
                try:
                    # Convert the combined number (e.g., "twelve million" → 12000000)
                    processed_words[-1] = str(w2n.word_to_num(combined_number))
                    i += 1  # Skip the next word since it's already processed
                    continue
                except ValueError:
                    pass  # If conversion fails, just continue processing

        # Handle compound numbers like "twenty-two"
        elif i + 1 < len(words):
            next_word = words[i + 1].lower().strip(",.!?")
            if lower_word in ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"] and next_word in word_to_num:
                processed_words.append(convert_word_to_number(f"{lower_word}-{next_word}"))
                i += 2  # Skip the next word as it's already processed
                continue  
        
       # Handle currency and numbers  
        if lower_word in currency_mapping and i > 0:  
            prev_word = words[i-1]  
            try:  
                number = str(w2n.word_to_num(prev_word.lower().strip(",.!?")))  # Convert word number to numeral  
            except ValueError:  
                number = prev_word if re.fullmatch(r'\d+(\.\d+)?', prev_word) else None  
  
            if number:  
                # Combine the number with the currency symbol  
                processed_words[-1] = currency_mapping[lower_word] + number  
                i += 1  # Skip the currency word  
                continue   
        
        # Convert word numbers to numerals  
        elif lower_word.isalpha():  
            try:  
                # Convert word number to numeral using word2number  
                number = str(w2n.word_to_num(lower_word))  
                processed_words.append(number)  
            except ValueError:  
                # If conversion fails, keep the word as is  
                processed_words.append(word)  
       
        # Handle time and measurement units
        elif lower_word in all_units:
            if i > 0 and (words[i-1].isdigit() or words[i-1].lower().strip(",.!?") in word_to_num):
                number = words[i-1] if words[i-1].isdigit() else word_to_num[words[i-1].lower().strip(",.!?")]
                processed_words[-1] = number + " " + lower_word
            else:
                processed_words.append(lower_word)

        # Handle numerals (digits) and convert word numbers
        elif word.isdigit():
            number = int(word)
            if 0 <= number <= 9 and (i + 1 >= len(words) or words[i + 1].lower() not in all_units.union(currency_mapping.keys())):
                processed_words.append(p.number_to_words(number))
            else:
                processed_words.append(word)

        elif lower_word in word_to_num:
            # Convert word numbers (0-9) only when followed by a unit or currency
            if i + 1 < len(words) and words[i + 1].lower() in all_units.union(currency_mapping.keys()):
                processed_words.append(word_to_num[lower_word])
            else:
                processed_words.append(lower_word)

        # Convert larger word-numbers like "eleven", "twenty-one", "million", "billion" to numerals
        elif lower_word.isalpha() and lower_word not in all_units and lower_word not in currency_mapping:
            processed_words.append(convert_word_to_number(lower_word))

        else:
            processed_words.append(word)  # No conversion needed
        
        i += 1

    return " ".join(processed_words)

# Example usage
if __name__ == "__main__":
    while True:
        try:
            user_input = input("Enter a sentence (numbers as words/numerals will be processed): ")
            print(f"Processed: {process_text(user_input)}")
        except Exception as e:
            print(f"An error occurred: {e}")
