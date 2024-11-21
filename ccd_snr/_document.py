import matplotlib.pyplot as plt
import pathlib
import aastex
import ccd_snr

__all__ = [
    "document",
    "pdf",
]


def document() -> aastex.Document:
    """
    An :mod:`aastex` representation of the article.
    """

    plt.rcParams["text.usetex"] = True
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.size"] = 9
    plt.rcParams["lines.linewidth"] = 1

    doc = aastex.Document(
        document_options=[
            "twocolumn",
        ],
        lmodern=False,
        textcomp=False,
    )

    doc.packages.append(aastex.Package("amsmath"))
    doc.packages.append(aastex.Package("hyperref"))

    doc.preamble += ccd_snr.acronyms()
    doc.variables += ccd_snr.variables()

    title = aastex.Title(
        "The Noise Measured by Backilluminated Silicon Sensors",
    )
    doc.append(title)

    doc += ccd_snr.authors()

    doc.append(ccd_snr.sections.abstract())
    doc.append(ccd_snr.sections.introduction())
    doc.append(ccd_snr.sections.model())
    doc.append(ccd_snr.sections.discussion())

    doc.append(aastex.Bibliography("sources"))

    return doc


def pdf() -> pathlib.Path:
    """
    Build a pdf version of :func:`document` and return the path of the document.
    """

    doc = document()

    path = pathlib.Path(__file__).parent / "ccd-euv-snr"
    doc.generate_pdf(
        filepath=path,
        clean_tex=False,
    )

    return path.with_suffix(".pdf")
