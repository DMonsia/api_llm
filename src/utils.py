from PyPDF2 import PdfReader


def read_text(file):
    return file.read()


def read_pdf(file):
    reader = PdfReader(file)
    return "\n\n".join(
        [reader.pages[i].extract_text() for i in range(len(reader.pages))]
    )

