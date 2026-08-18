import astropy.units as u
import named_arrays as na
from ._util import (
    _vmr_electron,
    _vmr_photon,
    _snr_improvement,
    _width_diffusion,
)

__all__ = [
    "wavelength",
    "width_pixel",
    "vmr_electron",
    "vmr_photon",
    "snr_improvement",
    "width_diffusion",
]

wavelength = [
    208,
    224,
    240,
    256,
    272,
    288,
    304,
    400,
]

wavelength = na.ScalarArray(wavelength * u.nm, axes="wavelength")

width_pixel = 15 * u.um

vmr_electron = _vmr_electron(wavelength, width_pixel)
vmr_photon = _vmr_photon(wavelength, width_pixel)

snr_improvement = _snr_improvement(wavelength, width_pixel)

width_diffusion = _width_diffusion(wavelength)
