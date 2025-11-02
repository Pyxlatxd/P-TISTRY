import re

def format_apa_italics(sentence):
    """
    Automatically detects and italicizes APA-style elements in a sentence.
    :param sentence: The sentence to be formatted.
    :return: Formatted sentence with APA-style italics.
    """
    italic_patterns = {
        "book": r"(?<=\b)(The Great Gatsby|To Kill a Mockingbird|Moby-Dick)(?=\b)",
        "journal": r"(?<=\b)(Journal of Psychology|Nature|Science)(?=\b)",
        "key_term": r"(?<=\b)(cognitive dissonance|operant conditioning|placebo effect)(?=\b)",
        "scale_anchor": r"(?<=\b)(strongly agree|neutral|strongly disagree)(?=\b)",
        "linguistic_example": r"(?<=\b)(elle parle français|je ne sais quoi|habeas corpus)(?=\b)"
    }
    
    for category, pattern in italic_patterns.items():
        sentence = re.sub(pattern, r"*\\1*", sentence)
    
    return sentence

def main():
    """Handles user input and prints formatted sentences."""
    while True:
        try:
            user_sentence = input("Enter a sentence (or type 'exit' to quit): ")
            if user_sentence.lower() == 'exit':
                print("Exiting program.")
                break
            if not user_sentence.strip():
                print("Error: Empty input. Please enter a valid sentence.")
                continue
            formatted_sentence = format_apa_italics(user_sentence)
            print("Formatted Sentence:", formatted_sentence, flush=True)
        except Exception as e:
            print(f"An error occurred: {e}", flush=True)

if __name__ == "__main__":
    print("Starting APA Italicization Program...", flush=True)
    main()
    print("Program has exited.", flush=True)
