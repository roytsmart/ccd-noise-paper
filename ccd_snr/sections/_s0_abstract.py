import aastex

__all__ = [
    "abstract",
]


def abstract() -> aastex.Abstract:
    result = aastex.Abstract()
    result.append(
        r"""
Silicon-based imaging sensors are a critical component for solar \UV\ astronomy.
Their high sensitivity and low noise are a vital part of making solar
\UV\ telescopes practical to build.
However, \UV\ light is unique compared to other components of the
electromagnetic spectrum since it has a shallow penetration depth
into the silicon substrate, which means that the corresponding electron-hole pairs
have a significant chance of recombination before being measured by the sensor.
In this article, we will estimate the noise measured by the theoretical silicon
sensor described in \citet{Stern1994} and show that modeling the recombination 
process is an important component of the expected total noise.
We will also introduce an easy-to-implement algorithm which can draw samples 
from the distribution of electrons measured for a given number of incident photons,
valid over the entire wavelength range of silicon sensors (0.1-1000 nm).
Finally, we will apply this model to the \AIA, \IRIS, and \MUSE\ instruments and 
calculate the expected slopes of the photon transfer curves for a few
wavelengths important to each instrument.
\acresetall
"""
    )
    return result
