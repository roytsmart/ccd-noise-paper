"""
Create the figures and compile the LaTeX files for this article.
"""

from ._wavelength import wavelength, energy
from ._ccd import ccd, ccd_aia
from . import diffusion
from ._vmr import vmr_stern
from . import simulations
from . import instruments
from . import tracks
from ._acronyms import acronyms
from ._variables import variables
from ._authors import authors
from . import figures
from . import tables
from ._keywords import keywords
from . import sections
from ._acknowledgements import acknowledgements
from ._document import document, pdf

__all__ = [
    "wavelength",
    "energy",
    "ccd",
    "ccd_aia",
    "diffusion",
    "vmr_stern",
    "simulations",
    "instruments",
    "tracks",
    "acronyms",
    "variables",
    "authors",
    "figures",
    "tables",
    "keywords",
    "sections",
    "acknowledgements",
    "document",
    "pdf",
]
