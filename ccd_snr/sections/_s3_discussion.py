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
Evaluating the same model without charge diffusion raises the predicted \IRIS\
ratio to approximately the measured value, so the disagreement could be
explained if we had overestimated the charge diffusion of the \IRIS\ \CCDs.
There are two reasons to suspect that we might have.
The thickness of the depletion region was fit to the measurements of
\citet{Stern2004}, which were made on a different sensor operated at a
different voltage, and the depletion thickness depends on both the resistivity
of the silicon and the applied bias.
Furthermore, we model the charge cloud as a Gaussian, whereas \citet{Pavlov1999}
show that the true radial distribution is peaked more strongly and has heavier
tails, which would place more of the charge liberated by a single photon in a
single pixel than we have assumed.
To test this, we measured the charge diffusion of the \IRIS\ \CCDs\ directly
using the tracks left by energetic particles (Appendix~\ref{appendix:tracks}).
On the \SJI\ \CCD, the sensor on which \citet{Wulser2018} measured the
photon-transfer curves, the probability that two electrons liberated at the
back surface are collected in the same pixel is
$\sjiSamePixel \pm \sjiSamePixelError$, compared to \sjiSamePixelModel\ for our
model.
This probability is measured without assuming a shape for the kernel and is the
quantity which enters Equation~\ref{eq:diffusedVmr}, so neither the depletion
thickness nor the shape of the kernel can account for the disagreement.

With the charge diffusion fixed by measurement, the measured ratio constrains
the remaining ingredients of Equation~\ref{eq:diffusedVmr}:
the quantum yield, which is well established at \wavelengthIrisRatio,
and the \CCE.
Reproducing the measured ratio would require the \CCE\ at the back surface to
be closer to unity than the \backsurfaceCCE\ implied by the \QE\ measurements
of \citet{Heymes2020}, so that nearly every photon liberates a full electron
and the \PCC\ contributes little to the variance.
Alternatively, the measurement itself may be biased.
The photon-transfer curve at \wavelengthIrisRatio\ was measured with a
deuterium lamp, whose illumination is less uniform and less stable than that of
the visible light-emitting diode used for the other curves, and any spatial or temporal
nonuniformity in the illumination adds variance which a photon-transfer curve
interprets as a larger \VMR.
We cannot distinguish between these possibilities with the published data,
and a photon-transfer measurement with a monochromatic, spatially uniform
\UV\ source on a sensor whose \CCE\ is independently known would settle the
question.
""")
    return result
