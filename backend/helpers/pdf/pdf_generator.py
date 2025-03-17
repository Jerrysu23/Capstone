# This file contains code that creates a PDF file given text. It is mostly used for the cover letter generator.
# An AI text response is generated representing the cover letter, and then a PDF is generated from that text.
# This file holds all functions necessary for interacting with pdf files for the cover letter generator.
#
# @Author: Preston Peck
# @Date: 2024-11-06

import fitz

def generate_pdf_from_text(content: str) -> bytes:
    """
    Generates a PDF file from the given text content.

    :param content: The text content to generate the PDF from.
    """
    try:

        pdf_document = fitz.open()

        # define page sizes and margins. CL will be 8.5x11 inches with 1 inch margins
        page_width, page_height = 8.5 * 72, 11 * 72
        page = pdf_document.new_page(width=page_width, height=page_height)
        rect = fitz.Rect(72, 72, page_width - 72, page_height - 72)

        # insert the formatted HTML cover letter text into the PDF
        css = "* {font-family: sans-serif;}"  # this may need to change dynamically in the future?
        page.insert_htmlbox(rect, content, css=css)

        # write to the pdf and obtain the pdf file's bytes
        pdf_bytes = pdf_document.write()
        pdf_document.close()

        return pdf_bytes
    
    except Exception as e:

        print(f"Error generating PDF: {e}")
        return None



def update_pdf():
    """
    Updates the PDF file with the new content.
    """

    pass
