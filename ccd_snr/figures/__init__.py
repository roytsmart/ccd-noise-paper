"""
Create the figures used in the article.
"""

from ._schematic import schematic
from ._qe_effective import qe_effective
from ._absorbance_and_cce import absorbance_and_cce
from ._noise_photon import noise_photon
from ._noise_electron import noise_electron
from ._noise_fano import noise_fano
from ._charge_diffusion import charge_diffusion
from ._kernel import diffusion_kernel

__all__ = [
    "qe_effective",
    "absorbance_and_cce",
    "noise_photon",
    "noise_electron",
    "noise_fano",
    "charge_diffusion",
    "diffusion_kernel",
]
