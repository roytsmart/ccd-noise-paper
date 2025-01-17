import aastex
import ccd_snr


def discussion() -> aastex.Section:
    result = aastex.Section("Results and Discussion")
    result.append(
        r"""     
Since $\text{EQE}(\lambda)$ is a type of efficiency,
it is tempting to treat the sensor like any other component in a given optical system
and simply use $\text{EQE}(\lambda)$ as another factor in the effective
area calculation.
This simple noise model is formalized in Equations 9 and 10 of \citet{Stern1986},
which gives the \VSR\ of the number of measured electrons as
\begin{equation} \label{eq:sternVSR}
    \text{VSR}(N_e'') = \text{IQY}(\lambda) + \mathcal{F} \quad \text{(incomplete!).}
\end{equation}
This is presumably the noise model used by most solar instrument teams.
For comparison, the \VSR\ predicted by our noise model is
\begin{equation} \label{eq:ourVSR}
    \text{VSR}(N_e'') = \left( \text{IQY}(\lambda) + \mathcal{F}_a - 1 \right) \text{CCE}(\lambda) + 1,
\end{equation}
where the apparent Fano factor,
\begin{equation}
    \mathcal{F}_a = \mathcal{F} + \frac{1/6}{\text{IQY}(\lambda)},
\end{equation}
accounts for additional noise due to electron discretization effects.
In Figures~\ref{fig:photonNoise} and~\ref{fig:electronNoise},
we have compared Equation~\ref{eq:sternVSR} (gray) 
to our model, Equation~\ref{eq:ourVSR} (black). 
Over most of the \SXR\ and visible wavelengths,
The \citet{Stern1986} model is a good approximation of the noise 
model developed in this work.
However, the effect of \PCC\ violates the assumptions of \citet{Stern1986}
and Equation~\ref{eq:sternVSR} overestimates the variance
predicted by our model by up to a factor of ${\sim}2$ in the \UV\ since the 
binomial distribution is narrower than the equivalent Poisson distribution,
especially as $\text{IQY}(\lambda)$ (the number of trials) approaches unity.
This is good news for engineers building \UV\ astronomical instruments since
there is much less noise than expected from the \citet{Stern1986} model in this 
wavelength range."""
    )
    result.append(ccd_snr.tables.fano_factor())
    result.append(
        r"""
In Table~\ref{table:instrumentVSR},
we have calculated the \VSR\ in terms of incident photons and measured electrons
for the target wavelengths of a few popular and upcoming solar instruments:
\AIA, \IRIS, and \MUSE\ \citep{DePontieu2020},
The results show that for the \EUV\ channels, \AIA\ and \MUSE\ are nearly
shot noise limited since the \VSR\ in units of incident photons is near unity.

Plotted in the right column of Table~\ref{table:instrumentVSR} is
the improvement factor between the \VSR\ of the \citet{Stern1986} noise model
and our noise model.
These ratios show that the \citet{Stern1986} model overestimates the variance
in the \AIA\ and \IRIS\ \FUV\ channels by about 50\%.
The \citet{Stern1986} model overestimates the variance even more
in the short-wavelength \EUV\ channels of \AIA\ and \MUSE.
Note that since the improvement factor is in variance units,
the improvement in \SNR\ is the square root of the improvement factor.

Table~\ref{table:instrumentVSR} also partially resolves a discrepancy
in the theoretical vs. measured noise in \IRIS.
In \citet{Wulser2018}, the authors measured a \VSR\ of \irisMeasuredVsr\
at \irisWavelength, expecting a \VSR\ of around \irisNaiveVsr.
In Table~\ref{table:instrumentVSR} we find that the theoretical \VSR\ of the
\IRIS\ sensor at \irisWavelength\ predicted by our model is \irisModeledVsr,
which is much closer to the measured value.
The remaining discrepancy may be due to charge diffusion as suggested by
\citet{Wulser2018}.

In retrospect, if we had grouped IQY and CCE together into an effecdtive QY, instead of A and CCE,
this confusion may not have happened.
ADD FIGURE SUPPORTING THIS.
"""
    )
    return result
