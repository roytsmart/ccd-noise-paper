"""
Create the figures and compile the LaTeX files for this article.
"""

from ._fano_factor import fano_factor
from ._wavelength import wavelength, energy
from ._ccd import ccd, ccd_aia
from ._diffusion import diffusion_kernel
from . import simulations
from ._acronyms import acronyms
from ._variables import variables
from ._authors import authors
from . import figures
from . import tables
from . import sections
from ._document import document, pdf

__all__ = [
    "fano_factor",
    "wavelength",
    "energy",
    "ccd",
    "ccd_aia",
    "diffusion_kernel",
    "simulations",
    "acronyms",
    "variables",
    "authors",
    "figures",
    "tables",
    "sections",
    "document",
    "pdf",
]
