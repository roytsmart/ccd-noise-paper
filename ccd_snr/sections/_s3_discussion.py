import aastex
import ccd_snr


def discussion() -> aastex.Section:
    result = aastex.Section("Results and Discussion")
    result.append(
        r"""
Since $\text{EQE}(\lambda)$ is a type of efficiency,
it's tempting to think that the variance of the signal measured by a silicon 
sensor is simply proportional to the product 
$\text{EQE}(\lambda) \times \langle N_\gamma \rangle$,
which we've plotted in Figures \ref{fig:photonNoise} and \ref{fig:electronNoise}
labeled as the ``naive'' model.
In most of the \SXR\ and visible wavelengths,
the naive model is a good approximation of the noise model developed in this work.
However, in the \UV\ wavelengths the naive model overestimates the variance
of the noise by up to a factor of $\sim 2$ since the binomial distribution
is much narrower than the Poisson distribution when the \CCE\ is low.
This is good news for engineers building \UV\ astronomical instruments since
there is much less noise than expected from the naive model in this wavelength
range.

In Table~\ref{table:instrumentVSR},
we've calculated the \VSR\ in terms of incident photons and measured electrons
for the target wavelengths of a few popular and upcoming solar instruments:
\AIA, \IRIS, and \MUSE.
The results show that for the \EUV\ channels, \AIA\ and \MUSE\ are nearly
shot-noise-limited since the \VSR\ in units of incident photons is near unity.

Table~\ref{table:instrumentVSR} also partially resolves a discrepancy
in the theoretical vs. measured noise in \IRIS.
In \citet{Wulser2018}, the authors measured a \VSR\ of of \irisMeasuredVsr\
expecting a \VSR\ of around \irisNaiveVsr.
In Table~\ref{table:instrumentVSR} we find that the theoretical \VSR\ of the
\IRIS\ sensor at \irisWavelength\ predicted by our model is \irisModeledVsr,
which is much closer to the measured value.
The remaining discrepancy may be due to charge diffusion as suggested by
\citet{Wulser2018}.

Taken together, Equation~\ref{eq:quantum-efficiency},
Algorithm~\ref{alg:electron-sample}, 
and Equation~\ref{eq:chargeDiffusionWidth} are enough to fully-describe our 
model of the sensor.
Algorithm~\ref{alg:electron-sample} samples the distribution of the number
of measured electrons given the expected number of incident photons.
Equation~\ref{eq:chargeDiffusionWidth} defines the spatial resolution of the
sensor,
and Equation~\ref{eq:quantum-efficiency} is used to invert 
Algorithm~\ref{alg:electron-sample} and compute the expected number of 
incident photons given the number of measured electrons.
"""
    )
    result.append(ccd_snr.tables.fano_factor())
    return result
