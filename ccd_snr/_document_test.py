import pathlib
import pymupdf
import pylatex
import ccd_snr


def test_document():
    doc = ccd_snr.document()
    assert isinstance(doc, pylatex.Document)


def test_pdf():
    pdf = ccd_snr.pdf()
    assert isinstance(pdf, pathlib.Path)
    assert pdf.exists()

    with pymupdf.open(pdf) as document:
        text = "".join(page.get_text() for page in document)

    # The bibliography and the cross-references are only resolved if the
    # article is compiled repeatedly with bibtex in between, which `latexmk`
    # does and a bare `pdflatex` does not. Without this check the article
    # builds "successfully" with every citation rendered as `(?)` and no
    # reference list at all.
    assert "REFERENCES" in text
    assert "(?)" not in text
    assert "??" not in text
