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
        uris = [
            link["uri"]
            for page in document
            for link in page.get_links()
            if "uri" in link
        ]

    # The bibliography and the cross-references are only resolved if the
    # article is compiled repeatedly with bibtex in between, which `latexmk`
    # does and a bare `pdflatex` does not. Without this check the article
    # builds "successfully" with every citation rendered as `(?)` and no
    # reference list at all.
    assert "REFERENCES" in text
    assert "(?)" not in text
    assert "??" not in text

    # The links to the API of optika point to the version the article was
    # built with. If `\optikaDocs` were not expanded, the links would start
    # with the name of the macro instead.
    uris_api = [uri for uri in uris if "_autosummary" in uri]
    assert uris_api
    for uri in uris_api:
        assert uri.startswith(f"{ccd_snr.url_docs_optika()}/_autosummary/")
