"""
title: PDF Reader Tool
author: Personal AI Agent
version: 1.0.0
description: Reads and extracts text from PDF files
"""

import fitz  # pymupdf
import os


class Tools:
    def __init__(self):
        pass

    def read_pdf(self, filepath: str) -> str:
        """
        Reads the content from a local PDF file.

        :param filepath: Absolute path to the PDF file
        :return: Extracted text from PDF
        """
        try:
            if not os.path.exists(filepath):
                return f"File not found: {filepath}"

            if not filepath.lower().endswith('.pdf'):
                return f"File is not a PDF: {filepath}"

            doc = fitz.open(filepath)
            text = ""
            page_count = len(doc)

            for page_num, page in enumerate(doc, 1):
                page_text = page.get_text()
                text += f"\n--- Page {page_num} ---\n{page_text}"

            doc.close()

            # Limit output to prevent context overflow
            max_chars = 8000
            if len(text) > max_chars:
                text = text[:max_chars] + f"\n\n[...truncated, {page_count} pages total]"

            return text.strip() if text.strip() else "PDF is empty or text could not be extracted."

        except Exception as e:
            return f"Error reading PDF: {str(e)}"
