from docx import Document
from features.level_headings import ai_format_headings

if __name__ == "__main__":
    doc = Document("groq_llama3_output.docx")
    doc = ai_format_headings(doc)
    doc.save("output_with_detections.docx")
    print("Processed document saved as output_with_detections.docx")
