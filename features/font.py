from docx import Document
from docx.shared import Pt, Inches, Mm
from docx.enum.text import WD_LINE_SPACING, WD_BREAK, WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from features.quotation import format_apa_quotations
from features.numeral import apply_apa_numerals

def rebuild_doc_with_apa(old_doc, font_name="Times New Roman", font_size=12, margin_in_inches=1.0):
    doc = Document()
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Inches(margin_in_inches)
    section.bottom_margin = Inches(margin_in_inches)
    section.left_margin = Inches(margin_in_inches)
    section.right_margin = Inches(margin_in_inches)

    # Add page numbers
    for section in doc.sections:
        section.different_first_page_header_footer = False
        header = section.header
        footer = section.footer
        for p in list(header.paragraphs):
            p._element.getparent().remove(p._element)
        for p in list(footer.paragraphs):
            p._element.getparent().remove(p._element)

        paragraph = header.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run = paragraph.add_run()
        fldChar_begin = OxmlElement("w:fldChar")
        fldChar_begin.set(qn("w:fldCharType"), "begin")
        run._r.append(fldChar_begin)
        instrText = OxmlElement("w:instrText")
        instrText.text = "PAGE"
        run._r.append(instrText)
        fldChar_end = OxmlElement("w:fldChar")
        fldChar_end.set(qn("w:fldCharType"), "end")
        run._r.append(fldChar_end)
        run.font.name = font_name
        run.font.size = Pt(font_size)

    in_references = False
    after_title_page = False
    previous_was_heading = False

    # Helper to detect Level 1–3 heading (bold + left/center)
    def is_heading_level_1_3(para):
        if not para.runs:
            return False
        run = para.runs[0]
        return run.bold and (para.alignment in [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER])

    def copy_paragraph(src_para, dst_doc, in_references=False, previous_was_heading=False):
        new_para = dst_doc.add_paragraph()
        pf_src = src_para.paragraph_format
        pf_dst = new_para.paragraph_format

        # --- Preserve spacing and alignment ---
        pf_dst.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        pf_dst.space_before = Pt(0)
        pf_dst.space_after = Pt(0)
        pf_dst.alignment = src_para.alignment or None
        pf_dst.left_indent = pf_src.left_indent or Inches(0)
        pf_dst.right_indent = pf_src.right_indent or Inches(0)

        # --- Determine first-line indent ---
        leading_spaces = len(src_para.text) - len(src_para.text.lstrip(" "))

        if in_references:
            # References section: hanging indent
            pf_dst.first_line_indent = Inches(-0.5)
        elif previous_was_heading:
            # Paragraph immediately after heading: standard APA indent
            pf_dst.first_line_indent = Inches(0.5)
        elif leading_spaces > 0:
            # Original leading spaces in paragraph
            pf_dst.first_line_indent = Inches(leading_spaces * 0.1)
        else:
            # No heading, no leading spaces: respect original or default 0.5"
            pf_dst.first_line_indent = pf_src.first_line_indent or Inches(0)

        # --- Copy runs with formatting and line breaks ---
        for run in src_para.runs:
            segments = run.text.split("\n")
            for i, seg in enumerate(segments):
                new_run = new_para.add_run(seg)
                new_run.bold = run.bold
                new_run.italic = run.italic
                new_run.underline = run.underline
                new_run.font.name = "Times New Roman"  # or use font_name
                new_run.font.size = Pt(12)            # or use font_size
                if i < len(segments) - 1:
                    new_run.add_break(WD_BREAK.LINE)

        # Handle empty paragraph
        if not src_para.runs and not src_para.text.strip():
            new_para.add_run("\u00A0")

        return new_para


    # --- Copy paragraphs ---
    for para in old_doc.paragraphs:
        text_lower = para.text.strip().lower()
        if text_lower.startswith("references"):
            in_references = True

        # Page break after title page
        if not after_title_page and ("introduction" in text_lower or "abstract" in text_lower):
            pb_para = doc.add_paragraph()
            pb_para.add_run().add_break(WD_BREAK.PAGE)
            after_title_page = True

        copy_paragraph(para, doc, in_references=in_references, previous_was_heading=previous_was_heading)
        previous_was_heading = is_heading_level_1_3(para)

    # --- Copy tables ---
    for table in old_doc.tables:
        new_table = doc.add_table(rows=len(table.rows), cols=len(table.columns))
        try:
            new_table.style = table.style
        except Exception:
            pass
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                new_cell = new_table.cell(r_idx, c_idx)
                for src_para in cell.paragraphs:
                    copy_paragraph(src_para, new_cell, in_references=in_references, previous_was_heading=False)

    # --- Final APA adjustments ---
    doc = format_apa_quotations(doc, font_name=font_name, font_size=font_size)
    doc = apply_apa_numerals(doc, font_name=font_name, font_size=font_size)

    return doc
