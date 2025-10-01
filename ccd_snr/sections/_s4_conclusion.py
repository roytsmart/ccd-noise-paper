import aastex

__all__ = [
    "conclusion",
]


def conclusion() -> aastex.Section:
    result = aastex.Section("Conclusion")
    result.packages.append(
        aastex.Package(name="algorithm2e", options="ruled"),
    )
    result.append(
        r"""
This work tries to realistically model a backilluminated silicon \CCD\ or \CMOS\ 
sensor in the simplest possible terms,
and is designed to serve as a plausible benchmark for more complicated simulations.
To model the noise intrinsic to the sensor, 
we have developed an easy-to-implement procedure,
described in Section~\ref{subsec:Noise},
which can sample the distribution of measured electrons with error much
less than the Fano noise, the smallest noise source considered in this work.
We have provided a reference implementation of our noise model in Python,
\href{https://optika.readthedocs.io/en/latest/_autosummary/optika.sensors.signal.html}{\texttt{optika.sensors.signal()}},
to make this noise model simple to integrate with existing instrument data
processing pipelines.

Our model shows that noise from \PCC\ effects is comparable
to the photon shot noise measured by the sensor in the \UV\ wavelength regime.
It also shows that current \CCD\ noise models,
such as \citet{Stern1986},
sometimes overestimate the noise measured by a silicon sensor in the \UV\ 
wavelength regime.
We recommend that astronomical instruments using backilluminated silicon sensors
operating in the \UV\ use our model instead of the simpler \citet{Stern1986}
noise model.
Real cameras introduce read noise which was not considered in this study.
A complete noise model would include read noise, which is not well-described
by a \VMR\ and depends on the exact details of the camera electronics.

We have also provided an estimate of the charge diffusion in a typical
backilluminated silicon sensor.
This is intended to be used along with the noise model in a forward model
of an astronomical instrument.
Quantifying the charge diffusion is important for an accurate noise model
since it represents the degree of correlation between adjacent pixels.

All of the code to model the backilluminated silicon sensors is implemented
in our Python package, 
\href{https://optika.readthedocs.io/en/latest/}{\texttt{optika}}.
The code to create this document, including the figures and tables,
is available at \url{https://github.com/roytsmart/ccd-noise-paper}.
"""
    )
    return result
