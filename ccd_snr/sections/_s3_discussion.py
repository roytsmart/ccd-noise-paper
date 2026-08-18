import aastex
import ccd_snr


def discussion() -> aastex.Section:
    result = aastex.Section("Results and Discussion")
    result.append(ccd_snr.figures.snr_improvement())
    result.append(ccd_snr.tables.vmr_predicted())
    result.append(ccd_snr.tables.vmr_measured())
    result.append(r"""Since $\text{EQE}(\lambda)$ can be interpreted as an efficiency,
it is tempting to think that the expected number of measured photons and their
variance is $\text{EQE} \times \E{N}_\gamma$.
However, using the effective \QE\ in this way is equivalent to an
all-or-nothing charge collection model where either all the electrons associated
with an absorbed photon are measured or none of them are.
This simple noise model is formalized in Equations 9 and 10 of \citet{Stern1986},
which gives the \VMR\ of the number of measured electrons as
\begin{equation} \label{eq:sternVMR}
    F_{e,\text{Stern}}'' = \overline{n} + \mathcal{F}
\end{equation}
This is the noise model used by \citet{Borders2010} and \citet{Wulser2018}.
For comparison, the
\VMR\ predicted by our undiffused noise model is the sum of
$F_{e,\text{shot}}''$ and $F_{e,\text{sensor}}''$,
\begin{equation} \label{eq:ourVMR}
    F(N_e'') = 1 + \bigl( \E{n} + \mathcal{F} - 1 \bigr) \bigl(\E{\eta} + F(\eta) \bigr).
\end{equation}
In Figure~\ref{fig:Noise},
we have compared $F_{e,\text{Stern}}''$ (dashed) 
to our undiffused model, $F(N_e'')$ (black). 
Over most of the \SXR\ and visible wavelengths
the \citet{Stern1986} model is a good approximation of the undiffused
model developed in this work since the penetration depth is deeper than
the \PCC\ region.
However, in the \UV, 
where the penetration depth is very shallow,
\citet{Stern1986} overestimates the noise compared to our undiffused model.

It may seem paradoxical to add a noise source and then measure less total noise,
but this is because more photons are measured in our model than the all-or-nothing
model.
Even though \PCC\ introduces noise, it is less noise than there would be if the
photon was undetected. 
This is good news for designers of \UV\ astronomical instruments since
there is less noise than expected from the \citet{Stern1986} model in this 
wavelength range.

In Figure~\ref{fig:SnrImprovement},
we have plotted the ratio of the \SNR\ predicted by our model to the \SNR\
predicted by the traditional model.
The blue line is the improvement ratio for the undiffused model and it shows
that there are two regions,
one from \qtyrange[range-units=single,range-phrase=-]{30}{100}{\angstrom} 
and another from \qtyrange[range-units=single,range-phrase=-]{500}{2000}{\angstrom},
where 

where the noise statistics deviate from the traditional model,
in some cases by up to ${\sim}30\%$.
This figure can be used to quickly estimate the importance of \PCC\ noise
in a given wavelength range.

In Table~\ref{table:instrumentVMR},
we have calculated the \VMR\
in terms of incident photons and measured electrons
for the target wavelengths of a few popular and upcoming solar instruments:
\AIA\ \citep{Lemen2012}, \IRIS\ \citep{DePontieu2014}, and \MUSE\ \citep{DePontieu2020}.
The results show that for the \EUV\ channels, \AIA\ and \MUSE\ are nearly
shot-noise-limited since the \VMR\ in units of incident photons is near unity.
Tabulated in the second-to-last column of Table~\ref{table:instrumentVMR} is
the improvement factor between the \VMR\ of the \citet{Stern1986} noise model
and our noise model.
These ratios show that the \AIA\ \qty{94}{\angstrom}
and \qty{1600}{\angstrom}, \IRIS\ \qty{1330}{\angstrom} and \qty{1400}{\angstrom},
and \MUSE\ \qty{108}{\angstrom} channels are predicted to have at least 20\% more \SNR\
than the traditional noise model would suggest.
These results include the influence of charge diffusion,
and we've also tabulated the size of the charge diffusion kernel in the last
column, since it sets the scale over which the charge from a single photon is
shared between neighboring pixels.

In Table~\ref{table:measurements},
we've attempted to reproduce the measurements of \citet{Wulser2018} and
\citet{Borders2010} by taking the ratio of the \VMR\ of a simulated \UV\ flat-field
image to the \VMR\ of a simulated visible flat-field image.
The flat-field images were created by drawing samples from
Equation~\ref{eq:measuredElectrons} and then diffusing each measured electron
individually, using the pixel size of the corresponding instrument.
This table shows that the discrepancy discussed in the introduction is
substantially reduced, though our model does not reproduce the measurements
exactly.
For \WFC, \citet{Borders2010} measured \measuredWfcRatio\ at \wavelengthWfcRatio\
where the traditional model expects about \expectedWfcRatio,
and our model predicts \modeledWfcRatio, close to the measured value.
For \IRIS, \citet{Wulser2018} measured \measuredIrisRatio\ at \wavelengthIrisRatio\
where the traditional model expects about \expectedIrisRatio,
and our model predicts \modeledIrisRatio.
This is much nearer the measurement than the traditional model,
but it underestimates it, where the traditional model overestimates it.
Our model therefore accounts for most of the reported discrepancy in both cases,
but it overcorrects for \IRIS.
The reason for the remaining disagreement is not well-understood.
One possibility is that the \QE\ of the sensors on \WFC\ and \IRIS\
is slightly different than that of the sensor measured by \citet{Heymes2020}.
Another is that the thickness of the depletion region differs from the one
measured by \citet{Stern2004}; a thicker depletion region would imply less
charge diffusion, which would raise our predicted ratios and improve the
agreement for \IRIS.
""")
    return result
