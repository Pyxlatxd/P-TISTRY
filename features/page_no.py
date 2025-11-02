from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches

def add_page_number(doc, font_name="Times New Roman", font_size=12, format_type="student", title_text=""):
    """
    APA-style header:
    - First line: running head (or empty for student) + page number far right.
    - Page number remains on same line even if running head wraps.
    - If running head exceeds 79 characters, overflow continues below automatically.
    """
    first_section = True
    for section in doc.sections:
        header = section.header
        for p in list(header.paragraphs):
            p._element.getparent().remove(p._element)

        # Create one paragraph for the header
        paragraph = header.add_paragraph()
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.paragraph_format.line_spacing = 1

        # Set a right-aligned tab stop at 6.5 inches (1-inch margins)
        paragraph.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_ALIGN_PARAGRAPH.RIGHT)

        # Running head logic
        running_head = ""
        if format_type.lower() == "professional" and title_text:
            if first_section:
                running_head = f"Running head: {title_text}"
                first_section = False
            else:
                running_head = title_text

        # Trim or wrap running head at around 87 characters
        if len(running_head) > 87:
            # Split long head into multiple lines but keep first line with tab
            first_line = running_head[:87]
            rest = running_head[87:]
            full_text = f"{first_line}\t"
        else:
            full_text = f"{running_head}\t"

        # Add first line + page number
        run_head = paragraph.add_run(full_text)
        run_head.font.name = font_name
        run_head.font.size = Pt(font_size)

        # Add page number field after tab (aligned right)
        run_page = paragraph.add_run()
        fldChar_begin = OxmlElement("w:fldChar")
        fldChar_begin.set(qn("w:fldCharType"), "begin")
        run_page._r.append(fldChar_begin)

        instrText = OxmlElement("w:instrText")
        instrText.text = "PAGE"
        run_page._r.append(instrText)

        fldChar_end = OxmlElement("w:fldChar")
        fldChar_end.set(qn("w:fldCharType"), "end")
        run_page._r.append(fldChar_end)

        run_page.font.name = font_name
        run_page.font.size = Pt(font_size)

        # If there’s remaining text beyond 79 chars, insert below
        if len(running_head) > 79:
            overflow_para = header.add_paragraph(rest)
            overflow_para.paragraph_format.space_before = Pt(0)
            overflow_para.paragraph_format.space_after = Pt(0)
            overflow_para.paragraph_format.line_spacing = 1
            for run in overflow_para.runs:
                run.font.name = font_name
                run.font.size = Pt(font_size)

    return doc
