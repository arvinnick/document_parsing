import fitz

from file_format import FileFormat


class PDF:
    """
    representation of PDF file
    instantiation arguments:
        - pdf_file_path: PDF file. each OCR object is bound to a single PDF file
    """
    searchable: bool
    file_format: FileFormat
    def __init__(self, pdf_file_path:str):
        self.pdf_file_path = pdf_file_path

    def __pdf_content_cacher(self):
        """caching the pdf content to reduce disk usage"""
        pass

    def __is_searchable__(self):
        """
        Private function. Examines the PDF file to be searchable. Returns True if it is, False otherwise
        """
        with fitz.open(self.pdf_file_path) as doc:
            if doc.is_pdf():
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
        pass

    def __detect_file_format(self):
        pass

    def parse(self):
        pass
