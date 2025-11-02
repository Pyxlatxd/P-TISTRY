from docx import Document
from features.font import rebuild_doc_with_apa
from features.page_no import add_page_number
from features.title import fix_title_page
from features.level_headings import ai_detect_and_apply_headings
from features.numeral import apply_apa_numerals
from features.quotation import format_apa_quotations

def build_apa_document(doc: Document, font_name="Times New Roman", font_size=12,
                       add_page_no=True, format_type="student"):
    """
    Rebuild a DOCX document with full APA compliance:
    1. Font & spacing
    2. Title page
    3. Apply APA numerals
    4. Format quotations
    5. Heading detection
    6. Page numbers (optional)
    """

    # Step 1: Font, spacing, etc.
    doc = rebuild_doc_with_apa(doc, font_name=font_name, font_size=font_size)

    # Step 2: Title page (returns title_text for running head)
    doc, title_text = fix_title_page(doc, font_name=font_name, font_size=font_size)

    # Step 3: Apply APA numerals
    doc = apply_apa_numerals(doc, font_name=font_name, font_size=font_size)

    # Step 4: Format quotations
    doc = format_apa_quotations(doc, font_name=font_name, font_size=font_size)

    # Step 5: Heading detection + formatting
    doc = ai_detect_and_apply_headings(doc, font_name=font_name, font_size=font_size)

    # Step 6: Page numbers
    doc = add_page_number(doc, font_name=font_name, font_size=font_size,
                              format_type=format_type, title_text=title_text)

    return doc
