# features/quotation_ai.py
import json
import re
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_LINE_SPACING
from features.api import GROQ_API_KEY
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)

# --- LLaMA helper ---
def identify_block_quotes(text: str):
    """
    Send the full document text to LLaMA.
    Returns a list of quotes that should be block quotes (≥40 words), including trailing citations.
    """
    prompt = f"""
    You are an expert in APA 7th edition formatting. Include trailing citations with the quote.
    Detect all direct quotations (enclosed in quotation marks) that are 40 words or more. Do not return anything shorter.

    Return a JSON like:
    {{
      "block_quotes": ["quote 1", "quote 2"]
    }}

    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    content = response.choices[0].message.content.strip()
    print("\n\n=== LLaMA RAW OUTPUT ===\n", content, "\n=========================\n")

    match = re.search(r'\{.*\}', content, re.DOTALL)
    if match:
        content = match.group(0)

    try:
        data = json.loads(content)
        print("Parsed JSON:", data)
        quotes = data.get("block_quotes", [])
        quotes = [q for q in quotes if len(q.split()) >= 40]
        return quotes
    except json.JSONDecodeError:
        print("JSONDecodeError — returning []")
        return []

# --- Insert paragraph after ---
def insert_paragraph_after(paragraph, text=None):
    new_para = paragraph._parent.add_paragraph(text)
    paragraph._p.addnext(new_para._p)
    return new_para

# --- Normalize text ---
def normalize_text(text):
    return text.replace("“", '"').replace("”", '"').replace("\n", " ").strip()

# --- Main formatting ---
def format_apa_quotations(doc: Document, font_name="Times New Roman", font_size=12):
    """
    Formats APA block quotes.
    1. Send full document text to LLaMA to identify block quotes.
    2. Scan paragraphs for quotes and trailing citations.
    3. Apply block formatting only to matching quotes ≥40 words.
    """
    # Step 1: get block quotes from LLaMA
    full_text = "\n".join(p.text for p in doc.paragraphs)
    block_quotes = [normalize_text(q) for q in identify_block_quotes(full_text)]
    if not block_quotes:
        return doc

    quote_pattern = r'[“"](.+?)[”"]|\'(.+?)\''

    for para in list(doc.paragraphs):
        para_text = normalize_text(para.text)
        matches = list(re.finditer(quote_pattern, para_text))
        if not matches:
            continue

        last_idx = 0
        new_segments = []

        # Step 2: split paragraph into segments
        for m in matches:
            quote_text = normalize_text(m.group(1) or m.group(2) or "")
            if not quote_text:
                continue

            start, end = m.start(), m.end()
            pre_text = para_text[last_idx:start].strip()
            if pre_text:
                new_segments.append((pre_text, False))

            # Check if LLaMA marked it as block quote
            is_block = any(quote_text in bq for bq in block_quotes)

            # Include trailing citation (parentheses)
            post_match = para_text[end:]
            citation_match = re.match(r'\s*\(.*?\)', post_match)
            if citation_match:
                quote_text += citation_match.group(0)
                end += citation_match.end()

            new_segments.append((quote_text, is_block))
            last_idx = end

        post_text = para_text[last_idx:].strip()
        if post_text:
            new_segments.append((post_text, False))
        
        # Step 3: rebuild paragraph(s) correctly
        current_para = para
        current_para.text = ""  # clear old text

        for seg_text, is_block in new_segments:
            word_count = len(seg_text.split())
            apply_block = is_block and word_count >= 40

            if apply_block:
                # Remove quotation marks for block quotes (APA rule)
                seg_text_clean = re.sub(r'^[“"\'\s]+|[”"\'\s]+$', '', seg_text.strip())

                new_p = insert_paragraph_after(current_para, seg_text_clean)
                pf = new_p.paragraph_format
                pf.left_indent = Inches(0.5)
                pf.first_line_indent = Inches(0)
                pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
                pf.space_before = Pt(0)
                pf.space_after = Pt(0)

                
            else:
    # Decide whether to insert a separating space.
    # Check paragraph text's last char (use .text which reflects the visible text).
                need_space = False
                if current_para.text:
                    last_char = current_para.text[-1]
                    if not last_char.isspace() and not seg_text.startswith(" "):
                        need_space = True

                to_add = (" " if need_space else "") + seg_text
                new_run = current_para.add_run(to_add)

                # apply font only to this new run (don't touch other runs)
                try:
                    new_run.font.name = font_name
                    new_run.font.size = Pt(font_size)
                except Exception:
                    pass

    return doc
