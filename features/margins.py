from docx.shared import Inches, Mm
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_docx_margins(doc, margin_in_inches: float = 1.0, title_page_paras: int = 10):
    """
    Apply APA margins and A4 page size.
    - margin_in_inches: margin for all sides
    - title_page_paras: number of paragraphs considered as title page (for section break)
    """
    for section in doc.sections:
        # Set A4 paper size
        section.page_width = Mm(210)
        section.page_height = Mm(297)

        # Set 1-inch (or custom) margins
        section.top_margin = Inches(margin_in_inches)
        section.bottom_margin = Inches(margin_in_inches)
        section.left_margin = Inches(margin_in_inches)
        section.right_margin = Inches(margin_in_inches)

    # Insert a section break after the title page so 2nd page is separate
    if doc.paragraphs and len(doc.paragraphs) >= title_page_paras:
        p = doc.paragraphs[title_page_paras - 1]._element
        sectPr = OxmlElement("w:sectPr")
        type_el = OxmlElement("w:type")
        type_el.set(qn("w:val"), "nextPage")
        sectPr.append(type_el)
        p.addnext(sectPr)

    return doc
