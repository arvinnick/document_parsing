import os
from pathlib import Path

import fitz
import ocrmypdf.api as ocr_api

from file_format import FileFormat


class PDF:
    """
    representation of PDF file
    instantiation arguments:
        - pdf_file_path: PDF file. each OCR object is bound to a single PDF file
    """
    file_format: FileFormat
    def __init__(self, pdf_file_path:Path):
        self.pdf_file_path = pdf_file_path
        self.searchable = self.__is_searchable__()

    def __pdf_content_cacher(self):
        """caching the pdf content to reduce disk usage"""
        pass

    def __is_searchable__(self):
        """
        Private function. Examines the PDF file to be searchable. Returns True if it is, False otherwise
        """
        with fitz.open(self.pdf_file_path) as doc:
            if doc.is_pdf:
                content = "".join([page.get_text() for page in doc])
            else:
                raise TypeError(f"{self.pdf_file_path} is not a PDF file")
        if not content:
            return False
        else:
            return True

    def get_searchable(self):
        """
        getter function, returning bool whether PDF text can be extracted or not
        :return:
        """
        return self.searchable

    def ocr(self):
        """
        performs OCR on self.pdf_file_path, making it searchable
        """
        if self.get_searchable():
            return
        else:
            ocr_exit_code = ocr_api.ocr(self.pdf_file_path, f"{self.pdf_file_path.name}_ocr.pdf")
            if ocr_exit_code != 0:
                raise RuntimeError(f"{ocr_exit_code}")
            else:
                self.searchable = True
                os.remove(self.pdf_file_path)
                os.rename(f"{self.pdf_file_path.name}_ocr.pdf", self.pdf_file_path.name)
                self.pdf_file_path = f"{self.pdf_file_path.name}_ocr.pdf"







    def __detect_file_format(self):
        pass

    def parse(self):
        pass
