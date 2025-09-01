import pymupdf4llm


def extract_text_from_pdf(file):
    doc = pymupdf4llm.to_markdown(file)
    return doc
