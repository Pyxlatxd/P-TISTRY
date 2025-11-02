import subprocess
import os

# Paths to the scripts
GETDOCX_PATH = r"/home/codespace/P-TISTRY/features/getdocx.py"
ITALICS_PATH = r"/home/codespace/P-TISTRY/features/italics.py"
# Extracted text file
EXTRACTED_TEXT_FILE = "extracted_text.txt"

if __name__ == "__main__":
    print("\nStarting Document Processing...")

    print("\nRunning getdocx.py...")
    try:
        subprocess.run(["python", GETDOCX_PATH], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nError running getdocx.py: {e}")
        exit(1)
        
    if not os.path.exists(EXTRACTED_TEXT_FILE):
        print(f"\nError: {EXTRACTED_TEXT_FILE} not found. Make sure getdocx.py ran successfully.")
        exit(1)

    print("\nRunning italics.py...")
    try:
        subprocess.run(["python", ITALICS_PATH], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nError running italics.py: {e}")
        exit(1)

    print("\nDocument processing complete. Check the updated .docx file.")