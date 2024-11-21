import aastex

__all__ = [
    "conclusion",
]


def conclusion() -> aastex.Section:
    result = aastex.Section("Conclusion")
    result.append(
        r"""
This work tries to realistically model a backilluminated \CCD\ or \CMOS\ sensor 
in the simplest possible terms,
and is designed to serve as a plausible benchmark for more complicated simulations.
To model the noise intrinsic to the sensor, 
we've developed an easy-to-implement procedure which can sample the distribution
of measured electrons with accuracy comparable to the Fano noise.
This model shows that noise from random recombination of electrons is comparable
to the photon shot noise measured by the sensor in the \UV\ wavelength regime.

We've also provided an estimate of the charge diffusion in a typical
backilluminated silicon sensor.
This is intended to be used along with the noise model in a forward model
of an astronomical instrument.

All of the code to model the backilluminated silicon sensors is implemented
in our Python package, 
\href{https://optika.readthedocs.io/en/latest/}{\texttt{optika}}.
The code to create this document, including the figures and tables,
is available at \url{https://github.com/byrdie/ccd-euv-snr-paper}.
"""
    )
    return result
