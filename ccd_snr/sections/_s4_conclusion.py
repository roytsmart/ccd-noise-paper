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
This work tries to realistically model a backilluminated \CCD\ or \CMOS\ sensor 
in the simplest possible terms,
and is designed to serve as a plausible benchmark for more complicated simulations.
To model the noise intrinsic to the sensor, 
we've developed an easy-to-implement procedure,
Equations~\ref{eq:shot-noise-variance}
and~\ref{eq:approxTotalElectrons}-\ref{eq:recombination}
(summarized in Algorithm~\ref{alg:electron-sample}),
which can sample the distribution of measured electrons with accuracy comparable 
to the Fano noise.
We've provided a reference implementation of Algorithm~\ref{alg:electron-sample} in Python,
\href{https://optika.readthedocs.io/en/latest/_autosummary/optika.sensors.electrons_measured.html}{\texttt{optika.sensors.electrons\_measured()}},
to make this noise model simple to integrate with existing instrument data
processing pipelines.

\begin{algorithm}
\caption{
A procedure to sample the distribution of the number of measured electrons
given an expected number of incident photons.
We've provided a reference implementation in Python,
\href{https://optika.readthedocs.io/en/latest/_autosummary/optika.sensors.electrons_measured.html}{\texttt{optika.sensors.electrons\_measured()}}.
}
\label{alg:electron-sample}
    \DontPrintSemicolon
    $\langle N_\gamma' \rangle \gets A(\lambda) \times \langle N_\gamma \rangle$\;
    $N_\gamma' \gets \texttt{poisson}(\langle N_\gamma' \rangle)$\;
    $\langle N_e \rangle \gets \text{IQY}(\lambda) \times N_\gamma'$\;
    $N_e \gets \texttt{poisson}(\langle N_e \rangle / \mathcal{F}') \times \mathcal{F}'$\;
    $N_e' \gets \lfloor  N_e \rfloor + \texttt{binomial}(1, \{ N_e \})$\;
    $N_e'' \gets \texttt{binomial}(N_e', \text{CCE}(\lambda))$\;
\end{algorithm}

Our noise model shows that noise from \PCC\ effects is comparable
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
by a \VSR\ and depends on the exact details of the camera electronics.

We've also provided an estimate of the charge diffusion in a typical
backilluminated silicon sensor.
This is intended to be used along with the noise model in a forward model
of an astronomical instrument.
Quantifying the charge diffusion is important for an accurate noise model
since it represents the degree of correlation between adjacent pixels.

All of the code to model the backilluminated silicon sensors is implemented
in our Python package, 
\href{https://optika.readthedocs.io/en/latest/}{\texttt{optika}}.
The code to create this document, including the figures and tables,
is available at \url{https://github.com/byrdie/ccd-euv-snr-paper}.
"""
    )
    return result
