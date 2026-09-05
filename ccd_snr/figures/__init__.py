"""
Create the figures used in the article.
"""

from ._schematic import schematic
from ._qe_effective import qe_effective
from ._absorbance_and_cce import absorbance_and_cce
from ._noise import noise
from ._energy_spectrum import energy_spectrum
from ._penetration_depth import penetration_depth
from ._charge_diffusion import charge_diffusion
from ._kernel import diffusion_kernel
from ._snr_improvement import snr_improvement
from ._tracks import tracks

__all__ = [
    "schematic",
    "qe_effective",
    "absorbance_and_cce",
    "noise",
    "energy_spectrum",
    "penetration_depth",
    "charge_diffusion",
    "diffusion_kernel",
    "snr_improvement",
    "tracks",
]
