import aastex
import ccd_snr


def discussion() -> aastex.Section:
    result = aastex.Section("Results and Discussion")
    result.append(
        r"""Since $\text{EQE}(\lambda)$ can be interpreted as an efficiency,
it is tempting to think that the expected number of measured photons and their
variance is $\text{EQE}(\lambda) \langle N_\gamma \rangle$.
However, using $\text{EQE}(\lambda)$ in this way is equivalent to an
all-or-nothing charge collection model where either all the electrons associated
with an absorbed photon are measured or none of them are.
This simple noise model is formalized in Equations 9 and 10 of \citet{Stern1986},
which gives the \VMR\ of the number of measured electrons as
\begin{equation} \label{eq:sternVMR}
    F_\text{Stern}'' = \overline{n} + \mathcal{F}
\end{equation}
In the absence of evidence to the contrary,
this is presumably the noise model used by most solar instrument teams.
For comparison, the \VMR\ predicted by our noise model 
(excluding charge diffusion)
is the sum of
$F_\text{shot}''$ and $F_\text{sensor}''$,
\begin{equation} \label{eq:ourVMR}
    F_\text{total}'' = f_{N_e''} = 1 - \mathcal{F} - f_\eta + \overline{n} \, \overline{\eta} + \overline{\eta} \mathcal{F} + \overline{n} f_\eta + \mathcal{F} f_\eta.
\end{equation}
In Figure~\ref{fig:Noise},
we have compared $F_\text{Stern}''$ (gray) 
to our model, $F_\text{total}''$ (black). 
Over most of the \SXR\ and visible wavelengths
the \citet{Stern1986} model is a good approximation of the noise 
model developed in this work since the penetration depth is deeper than
the \PCC\ region.
However, in the \UV, 
where the penetration depth is very shallow,
the \citet{Stern1986} overestimates the noise compared to our model.

It may seem paradoxical to add a noise source and then measure less total noise,
but this is because more photons are measured in our model than the all-or-nothing
model.
Even though \PCC\ introduces noise, it is less noise than there would be if the
photon was undetected. 
This is good news for engineers building \UV\ astronomical instruments since
there is much less noise than expected from the \citet{Stern1986} model in this 
wavelength range."""
    )
    result.append(ccd_snr.figures.snr_improvement())
    result.append(
        r"""In Figure~\ref{fig:SnrImprovement},
we have plotted the ratio of the \SNR\ predicted by our model to the \SNR\
predicted by the traditional model.
It shows that our model predicts that there are two regions,
one from \qtyrange[range-units=single,range-phrase=-]{30}{100}{\angstrom} 
and another from \qtyrange[range-units=single,range-phrase=-]{500}{2000}{\angstrom},
where the noise statistics deviate from the traditional model,
in some cases by up to ${\sim}30\%$.
This figure can be used to quickly estimate the importance of \PCC\ noise
in a given wavelength range."""
    )
    result.append(ccd_snr.tables.fano_factor())
    result.append(
        r"""
In Table~\ref{table:instrumentVMR},
we have calculated the \VMR\
in terms of incident photons and measured electrons
for the target wavelengths of a few popular +and upcoming solar instruments:
\AIA\ \citep{Lemen2012}, \IRIS\ \citep{DePontieu2014}, and \MUSE\ \citep{DePontieu2020}.
The results show that for the \EUV\ channels, \AIA\ and \MUSE\ are nearly
shot-noise-limited since the \VMR\ in units of incident photons is near unity.
Plotted in the second-to-last column of Table~\ref{table:instrumentVMR} is
the improvement factor between the \VMR\ of the \citet{Stern1986} noise model
and our noise model.
These ratios show that the \AIA\ \qty{94}{\angstrom}
and \qty{1600}{\angstrom}, \IRIS\ \qty{1330}{\angstrom} and \qty{1400}{\angstrom},
and \MUSE\ \qty{108}{\angstrom} channels are predicted to have at least 20\% more \SNR\
than the traditional noise model would suggest.
These results do not include the influence of charge diffusion,
so we've included the size of the charge diffusion kernel in the last column
which can be used in a forward model of these instrument
to blur the result after the noise has been applied."""
    )
    result.append(ccd_snr.tables.measurements())
    result.append(r"""
In Table~\ref{table:measurements},
we've attempted to reproduce the measurements of \citet{Wulser2018} and
\citet{Borders2010} by taking the ratio of the \VMR\ of an \UV\ flat-field
image to the \VMR\ of a visible flat-field image.
The flat-field images were created by drawing samples from Equation~\ref{eq:measuredElectrons},
and then convolving with the appropriate charge-diffusion kernel,
such as Figure~\ref{fig:chargeDiffusionKernel} for \IRIS.
This table shows that the discrepancy discussed in the introduction is mostly
resolved.
For \IRIS, \citet{Wulser2018} measured \measuredIrisRatio\ at \wavelengthIrisRatio\ expecting about
\expectedIrisRatio, but our model predicted \modeledIrisRatio, which is much closer.
Similarly for \WFC, \citet{Borders2010} measured \measuredWfcRatio\ at \wavelengthWfcRatio\ expecting about
\expectedWfcRatio\ and our model predicted \modeledWfcRatio, which again is closer than their expected value.
The reason for the remaining discrepancy is not well-understood,
but one obvious
but one possibility is that the details of the \PCC\ region are different in
reality, and we may need to move beyond the \citet{Stern1994} model. 
"""
    )
    return result
