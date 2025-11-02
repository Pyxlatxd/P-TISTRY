# Handle word phrases with `parse()` for 10 or more (multi-word numbers)
        elif lower_word.isalpha():  # If the word consists only of letters (no digits)
            try:
                # Use `parse` method to parse numbers 10 or more (e.g., "three hundred")
                numeric_value = p.parse(word)
                if numeric_value >= 10:  # Only convert for 10 or more
                    processed_words.append(str(numeric_value))
                else:
                    processed_words.append(word)  # Keep it as a word if it's less than 10
            except ValueError:
                processed_words.append(word)  # If not a valid number phrase, keep as word


 # Handle "number word + currency symbol" (e.g., "three $")
        elif lower_word in word_to_num and (i + 1 < len(words) and words[i + 1].strip(",.!?") in currency_words.values()):
            # Convert the word to a number and place the currency symbol before it
            processed_words.append(currency_words[words[i + 1].lower()])  # Add the currency symbol
            processed_words.append(word_to_num[lower_word])  # Convert the word to a number
            i += 1  # Skip the next word (currency symbol) since we've already added it