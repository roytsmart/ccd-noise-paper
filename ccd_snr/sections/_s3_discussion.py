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
However, using $\text{EQE}(\lambda)$ in this way is equivalent to an
all-or-nothing charge collection model where either all the electrons associated
with an absorbed photon are measured or none of them are.
This simple noise model is formalized in Equations 9 and 10 of \citet{Stern1986},
which gives the \VMR\ of the number of measured electrons as
\begin{equation} \label{eq:sternVMR}
    \text{VMR}(N_e'') = \text{IQY}(\lambda) + \mathcal{F} \quad \text{(incomplete!).}
\end{equation}
In the absence of evidence to the contrary,
this is presumably the noise model used by most solar instrument teams.
For comparison, the \VMR\ predicted by our noise model is
\begin{equation} \label{eq:ourVMR}
    \text{VMR}(N_e'') = \text{IQY}(\lambda) + \frac{\text{VBS}(\mu_Q, \mu_H, \sigma_Q^2, \sigma_H^2)}{\text{EBS}(\mu_Q, \mu_H)},
\end{equation}
where
\begin{equation}
    \mu_Q = \text{IQY}(\lambda),
\end{equation}
\begin{equation}
    \sigma_Q^2 = \mu_Q \mathcal{F} + \frac{1}{6},
\end{equation}
\begin{equation}
    \mu_H = \text{CCE}(\lambda),
\end{equation}
and
\begin{equation}
    \sigma_H^2 = 2 e^{-\alpha W} \left( \frac{1 - \eta_0}{\alpha W} \right)^2 \bigl( \sinh(\alpha W) - \alpha W \bigr).
\end{equation}
In Figure~\ref{fig:Noise},
we have compared Equation~\ref{eq:sternVMR} (gray) 
to our model, Equation~\ref{eq:ourVMR} (black). 
Over most of the \SXR\ and visible wavelengths,
The \citet{Stern1986} model is a good approximation of the noise 
model developed in this work.
However, the effect of \PCC\ violates the assumptions of \citet{Stern1986}
and Equation~\ref{eq:sternVMR} overestimates the variance
predicted by our model by up to a factor of ${\sim}2$ in the \UV\ since treating
each photon as a binary choice introduces more noise than treating each electron
as a binary choice.
This is good news for engineers building \UV\ astronomical instruments since
there is much less noise than expected from the \citet{Stern1986} model in this 
wavelength range."""
    )
    result.append(ccd_snr.tables.fano_factor())
    result.append(ccd_snr.tables.measurements())
    result.append(
        r"""
In Table~\ref{table:instrumentVMR},
we have calculated the \VMR\ in terms of incident photons and measured electrons
for the target wavelengths of a few popular and upcoming solar instruments:
\AIA\ \citep{Lemen2012}, \IRIS\ \citep{DePontieu2014}, and \MUSE\ \citep{DePontieu2020}.
The results show that for the \EUV\ channels, \AIA\ and \MUSE\ are nearly
shot noise limited since the \VMR\ in units of incident photons is near unity.

Plotted in the right column of Table~\ref{table:instrumentVMR} is
the improvement factor between the \VMR\ of the \citet{Stern1986} noise model
and our noise model.
These ratios show that the \citet{Stern1986} model overestimates the variance
in the \AIA\ and \IRIS\ \FUV\ channels by about 50\%.
The \citet{Stern1986} model overestimates the variance even more
in the short-wavelength \EUV\ channels of \AIA\ and \MUSE.
Note that since the improvement factor is in variance units,
the improvement in \SNR\ is the square root of the improvement factor.

Table~\ref{table:instrumentVMR} also partially resolves a discrepancy
in the theoretical vs. measured noise in \IRIS.
In \citet{Wulser2018}, the authors measured a \VMR\ of \irisMeasuredVmr\
at \irisWavelength, expecting a \VMR\ of around \irisNaiveVmr.
In Table~\ref{table:instrumentVMR} we find that the theoretical \VMR\ of the
\IRIS\ sensor at \irisWavelength\ predicted by our model is \irisModeledVmr,
which is much closer to the measured value.
The remaining discrepancy may be due to charge diffusion as suggested by
\citet{Wulser2018}.
"""
    )
    return result
