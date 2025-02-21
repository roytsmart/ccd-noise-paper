"""
Create the figures and compile the LaTeX files for this article.
"""

from . import random
from ._fano_factor import fano_factor
from ._wavelength import wavelength, energy
from ._ccd import ccd, ccd_aia
from . import diffusion
from . import simulations
from . import instruments
from ._acronyms import acronyms
from ._variables import variables
from ._authors import authors
from . import figures
from . import tables
from . import sections
from ._document import document, pdf

__all__ = [
    "random",
    "fano_factor",
    "wavelength",
    "energy",
    "ccd",
    "ccd_aia",
    "diffusion",
    "simulations",
    "instruments",
    "acronyms",
    "variables",
    "authors",
    "figures",
    "tables",
    "sections",
    "document",
    "pdf",
]
