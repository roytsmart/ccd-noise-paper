import aastex

__all__ = [
    "model",
]

import ccd_snr.figures


def model() -> aastex.Section:
    result = aastex.Section("CCD Model")
    result.append(
        r"""
In this work, we will model the light-sensitive region of the backilluminated 
sensor as a epitaxial silicon layer with a thickness $D$, which is coated
with a thin oxide layer of thickness $\delta$ to provide a realistic transmission 
coefficient.
The illuminated side of the epitaxial layer is considered to have a \PCC\ region
of width $W$, where some of the generated electron-hole pairs recombine before being
measured by the sensor.
In this work we will adopt the convention where unprimed variables
represent quantities incident on the sensor,
primed variables represent quantities internal to the sensor,
and the double-primed variables represent quantities measured by the sensor. 
In Section~\ref{subsec:Signal} we will model the \QE\ of a silicon sensor using 
the method described in \citet{Stern1994},
in Section~\ref{subsec:Noise} we will see how the \citet{Stern1994} \QE\ model
affects the variance of the signal measured by the sensor,
and in Section~\ref{subsec:ChargeDiffusion} we will model the charge diffusion
of the sensor which is needed for a complete description of the noise.
"""
    )
    result.append(ccd_snr.figures.schematic())
    subsection_qe = aastex.Subsection("Signal")
    subsection_qe.append(ccd_snr.figures.absorbance_and_cce())
    subsection_qe.append(ccd_snr.figures.qe_effective())
    subsection_qe.append(ccd_snr.tables.models())
    subsection_qe.append(
        r"""
\QE\ is the average number of photoelectrons measured per photon and is a common 
performance metric for measuring sensor sensitivity.
It is given in \citet{Janesick2001} as
\begin{equation} \label{eq:quantum-efficiency}
    \text{QE}(\lambda, T) = \biggl \langle \frac{N_{e}''}{N_\gamma} \biggr \rangle
                          = A(\lambda) \, \overline{n}(\lambda, T) \, \overline{\eta}(\lambda),
\end{equation}
where $\lambda$ is the wavelength of the incident photons in vacuum,
$T$ is the temperature of the sensor,
$\langle \cdot \rangle$ denotes an expectation value,
$N_e''$ is the number of electrons measured by the sensor,
$N_\gamma$ is the total number of photons incident on the sensor,
$A(\lambda)$ is the fraction of incident energy absorbed by the light-sensitive 
layer, 
$\overline{n}(\lambda, T)$ is the average quantum yield,
the number of photoelectrons generated per absorbed photon,
and $\overline{\eta}(\lambda)$ is the average \CCE,
the fraction of generated photoelectrons measured by the sensor.

The absorbance $A(\lambda)$ can be determined from the optical constants of Si 
and $\text{SiO}_2$, using, for example, the popular IMD code \citep{Windt1998}.
For this work, we used our Python library, 
\texttt{optika} \citep{optika}, 
which uses the transfer matrix method described in \citet{Yeh1988} 
with the optical constants from \citet{Palik1997}, \citet{Henke1993}, and 
\citet{Rodriguez-deMarcos2016} to compute the electric field for every interface
in the sensor.
In Figure \ref{fig:absorbanceAndCCE} we have plotted $A(\lambda)$ for the 
\cite{Heymes2020} parameters in Table \ref{table:models}.

In \citet{Stern1994}, the authors assume no reflections from the unilluminated
side of the sensor for simplicity.
In this work, we compute the total change in Poynting flux into and out of the 
light-sensitive region of the sensor to determine $A(\lambda)$.
This treatment introduces interference effects for infrared wavelengths, 
which can be seen on the right side of Figure \ref{fig:absorbanceAndCCE}.

Determining $\overline{n}(\lambda, T)$ over the entire wavelength range considered 
in this study is an area of ongoing research \citep[just to name a few]{Fraser1994,Geist1996,Scholze1998,Fang2019}.
This work will use the quantum yield model developed by \citet{Ramanathan2020}
which uses a phenomenological model of impact ionization to bridge the ``UV gap'',
an area where direct measurements of the quantum yield are not yet available.
They give the average quantum yield as 
\begin{equation} \label{eq:iqy}
    \overline{n}(E, T) = \begin{cases}
        \sum_{n=0}^\infty n p_n(E, T), & 0 < E \le \qty{50}{\electronvolt} \\
        E / \epsilon_{eh}(T), & \qty{50}{\electronvolt} < E < \infty,
    \end{cases}
\end{equation}
where $E$ is the energy of the incident photon,
$n$ is the actual quantum yield,
$p_n(E, T)$ is a table of pair-creation probabilities which is provided in their supplementary material,
\begin{equation}
    \epsilon_{eh}(T) = 1.7 E_g(T) + (\qty{0.084}{\per\electronvolt}) A + \qty{1.3}{\electronvolt},
\end{equation}
is the asymptotic pair-production energy,
\begin{equation}
    E_g(T) = \qty{1.1692}{\electronvolt} - \frac{(\qty{4.9e-4}{\electronvolt\per\kelvin}) \, T^2}{T + \qty{655}{\kelvin}},
\end{equation}
is the bandgap energy of silicon,
and $A = \qty{5.2}{\square\electronvolt}$.

In \citet{Stern1994}, the average \CCE\ is expressed in terms of a differential \CCE,
$\eta(z)$, which is the fraction of photoelectrons collected for a photon 
absorbed at a depth $z$ into the epitaxial layer.
The average \CCE\ is then the first moment of the differential \CCE\ weighted by 
the probability of absorbing a photon at a depth $z$,
\begin{equation} \label{cce}
    \overline{\eta}(\lambda) = \frac{\int_0^\infty \eta(z) \, e^{-\alpha(\lambda) z} \, dz}
                               {\int_0^\infty e^{-\alpha(\lambda) z} \, dz},
\end{equation}
where $\alpha(\lambda)$ is the absorption coefficient of silicon for the given 
wavelength.

In principle, $\eta(z)$ is a function of the exact implant profile which is
usually impractical to measure, but see \cite{Stern2004,Boerner2012} for a case 
where the authors did have a measurement of the implant profile provided 
by the manufacturer.
In \citet{Stern1994}, the authors instead adopt a piecewise-linear approximation 
of the differential \CCE,
\begin{equation} \label{differential-cce}
    \eta(z) = \begin{cases}
        \eta_0 + (1 - \eta_0) z / W, & 0 < z < W \\
        1, & W < z < \infty
    \end{cases}
\end{equation}
where $\eta_0$ is the differential \CCE at the back surface of the sensor.
Plugging Equation \ref{differential-cce} into Equation \ref{cce} yields an
arithmetic expression for the \CCE,
\begin{equation}
    \overline{\eta}(\lambda) = \eta_0 + \left( \frac{1 - \eta_0}{\alpha W} \right)(1 - e^{-\alpha W}),
\end{equation}
which can be used in Equation \ref{eq:quantum-efficiency} to determine the \QE.
In Figure \ref{fig:absorbanceAndCCE} we have plotted the average \CCE\ for
the \citet{Heymes2020} parameters in Table \ref{table:models}.

In \citet{Stern1994}, the authors define an effective \QE\ as
\begin{equation} \label{eqe}
    \text{EQE}(\lambda) = A(\lambda) \, \overline{\eta}(\lambda),
\end{equation}
which is the quantity that is typically measured when calibrating a image sensor
\citep{Stern1994,Stern2004,Boerner2012}.
In Figure~\ref{fig:eqe}, we have plotted the measured, effective \QE\ for two
sources: \citet{Boerner2012} which measured the \AIA\ \CCDs\ at a few
discrete wavelengths, and \citet{Heymes2020} which measured a Teledyne e2v CCD97
sensor over a wide wavelength range with high resolution using a monochromator.

Using the Nelder-Mead minimization algorithm \citep{Gao2010},
we found the free parameters of our model which best fit the data in 
\citet{Boerner2012} and \citet{Heymes2020}.
These models are plotted as solid lines in Figure~\ref{fig:eqe},
and the corresponding values of the free parameters are shown in 
Table~\ref{table:models}.
Throughout the remainder of this work we will use the model which best fits
the \citet{Heymes2020} data.
"""
    )
    result.append(subsection_qe)

    subsection_noise = aastex.Subsection("Noise")
    subsection_noise.append(ccd_snr.figures.noise())
    subsection_noise.append(ccd_snr.figures.energy_spectrum())
    subsection_noise.append(
        r"""
Our noise model will consider three sources:
shot noise from the random arrival time of the photons striking the sensor,
Fano noise due to inherent randomness in the process which converts photons
to electrons,
and noise due to electrons randomly recombining before they can be measured by
the sensor.
This section will describe the statistics of each noise source and demonstrate
a procedure which can simulate the noise measured by our model sensor
for a given number of incident photons.

Throughout this work, we will measure noise in terms of a \VSR,
\begin{equation}
    \text{VSR}(X) = \frac{\text{Var}(X)}{\langle X \rangle},
\end{equation}
where $X$ is some random variable
and $\text{Var}(X)$ is the variance of $X$.
Using the \VSR\ to express the noise is convenient since it is constant as a 
function of signal for most of the distributions studied here.
For example, the \VSR\ of a Poisson random variable is always unity since its 
variance and expectation value are equal.
The \VSR\ is not dimensionless
(it has the same units as $X$),
so we must take care to interpret the \VSR\ in terms of the correct units.

In Figure~\ref{fig:Noise} we have plotted
the \VSR\ for the noise sources considered in this study in two different units:
number of incident photons and number of measured electrons.
Figure~\ref{fig:Noise}a is useful if you are \textit{designing} an instrument since
you presumably know the radiance of the source and the effective area of the
rest of your instrument, and you want to know how much noise to expect in
terms of the number of photons incident on the sensor.
Figure~\ref{fig:Noise}b is useful if you are \textit{calibrating} an instrument
and want to know how much noise to expect for a given number of measured
electrons.
The details of the calculations for Figure~\ref{fig:Noise} are presented in the 
subsections below.
"""
    )
    subsubsection_noise_shot = aastex.Subsubsection("Shot Noise")
    subsubsection_noise_shot.append(
        r"""
Shot noise from the random arrival time of each photon is often the leading 
noise contributor in \UV\ solar astronomy \citep{Lemen2012, DePontieu2014}.
The number of photons that interact with the silicon, 
$N_\gamma'$, is drawn from a Poisson distribution,
\begin{equation} \label{eq:shot-noise-variance}
    N_\gamma' \leftarrow \text{Pois}(A(\lambda) \langle N_\gamma \rangle),
\end{equation}
where the expected value is the product of absorbance $A(\lambda)$ 
and the expected number of \textit{incident} photons, $\langle N_\gamma \rangle$.

We can compute the \VSR\ of the shot noi
In Figure~\ref{fig:Noise}
we have plotted the \VSR\ of the shot noise in blue.
In Figure~\ref{fig:Noise}a, we can see that the \VSR\ of the shot noise
relative to the number of incident photons is often unity since it is
fundamentally a Poisson process.
The shot noise only deviates from unity when $A(\lambda)$ is significantly
less than one
(like in the \UV),
leading to more noise for a given number of incident photons.
"""
    )
    subsection_noise.append(subsubsection_noise_shot)
    subsubsection_noise_fano = aastex.Subsubsection("Fano Noise")
    subsubsection_noise_fano.append(
        r"""
The energy resolution of silicon detectors is ultimately limited due to Fano
noise \citep{Fano1947}, the unpredictable variation of the quantum yield, 
the number of electrons generated per absorbed photon.
Fano noise is usually expressed in terms of the Fano factor, 
$\mathcal{F} = \text{VSR}(n)$.
Silicon is commonly accepted to have $\mathcal{F} \approx 0.1$ \citep{Janesick2001}.
In part due to variations of the Fano noise as a function of wavelength and
temperature \citep{Fraser1994}, 
there is some disagreement in the literature around a more precise value for
$\mathcal{F}$ 
\citep[\& references therein]{Fraser1994,Lowe1997,Mazziotta2008,Kotov2018,Rodrigues2021,Rodrigues2023}.
However, because the Fano noise is so small compared to the other noise sources
considered in this study, the precise form of this noise model does not
appreciably influence our conclusions.

As we mentioned in Section~\ref{subsec:Signal},
this work uses the quantum yield model of \citet{Ramanathan2020}.
They provide the \PMF\ of the quantum yield distribution, $p_n(E, T)$, which we can use
directly to generate random samples of the quantum yield for $E \le \qty{50}{\electronvolt}$.
For $E > \qty{50}{\electronvolt}$, we will assume that the quantum yield
is a Gaussian distribution centered around $\overline{n}(\lambda, T)$,
with standard deviation $\sqrt{\overline{n}(\lambda, T) \, \mathcal{F}(T)}$,
where $\mathcal{F}(T)$ is the asymptotic Fano factor given by \citet{Ramanathan2020} as
\begin{equation}
    \mathcal{F}(T) = (\qty{-0.028}{\per\electronvolt}) \, E_g(T) + (\qty{0.0015}{\per\square\electronvolt}) \, A + 0.14.
\end{equation}
At \qty{300}{K}, this corresponds to a Fano factor of approximately 0.114,
which is generally consistent with the best-available measurement of the
Fano factor by \citet{Rodrigues2021} at \SI{6}{\kilo\electronvolt}.

In Figure~\ref{fig:Noise} we've plotted the Fano factor in green.
This shows that the Fano noise is the smallest contributor to the total noise
across the entire wavelength range and is often at least an order of magnitude
smaller than the other noise sources.
Only in the \UV, where the Fano factor roughly doubles around \qty{2000}{\angstrom}, 
is the Fano noise an appreciable fraction of the total noise.
"""
    )
    subsection_noise.append(subsubsection_noise_fano)
    subsubsection_noise_recombination = aastex.Subsubsection(
        "Partial-Charge Collection Noise",
    )
    subsubsection_noise_recombination.append(
        r"""
Random recombination of photoelectrons in the \PCC\ region is a significant source of noise in
the \UV\ since the photons are absorbed so close to the surface,
where the \CCE\ is relatively low (Figure \ref{fig:absorbanceAndCCE}).
In the \citet{Stern1994} charge-collection model, 
each photoelectron generated in the \PCC\ region has a probability 
$\eta(z)$ of \textit{not} recombining and subsequently being measured 
by the sensor.
If $n_i'$ is the quantum yield of the $i$th photon generated using
the \citet{Ramanathan2020} model discussed in the previous section,
we can express the \textit{measured} quantum yield as
\begin{equation} \label{eq:measuredQuantumYield}
    n_i'' \leftarrow \text{B}(n_i', \eta(z_i)),
\end{equation}
where
$z_i$ is the penetration depth of the $i$th photon.
and $\text{B}(n, p)$ is a sample from the binomial distribution
with $n$ trials and probability of success $p$.
We can use \ref{eq:measuredQuantumYield} to compute the total number of measured
electrons given $N_\gamma'$ absorbed photons as
\begin{equation} \label{eq:measuredElectrons}
    N_e'' = \sum_{i=0}^{N_\gamma'} n_i''.
\end{equation}
This expression is intended to be used in an instrument forward model to sample 
the distribution of measured electrons given an expected number of incident photons.

In Figure~\ref{fig:energySpectrum},
we have plotted the probability of measuring a given number of electrons
using Monte Carlo simulations of Equation~\ref{eq:measuredElectrons} 
and the \citet{Stern1986} noise model
to demonstrate the quality of our approximation.
In the \FUV\ and \EUV\ we can see that this approximation is extremely accurate,
only in the \SXR\ does this approximation deviate slightly from the true
distribution.

To ease adoption of this model,
we've provided a reference implementation of Equation~\ref{eq:measuredElectrons}
in Python,
\href{https://optika.readthedocs.io/en/latest/_autosummary/optika.sensors.signal.html}{\texttt{optika.sensors.signal()}},
which is designed to be simple to use for existing and future instrument pipelines.

In Figure~\ref{fig:Noise} we have plotted the \VSR\ of the recombination noise
in orange.
This figure shows that recombination noise
is the dominant source of noise measured by the sensor
in the \FUV\ and remains non-negligible into the \EUV.
"""
    )
    subsection_noise.append(subsubsection_noise_recombination)
    result.append(subsection_noise)

    subsection_charge_spreading = aastex.Subsection("Charge Diffusion")
    subsection_charge_spreading.append(
        r"""
In most backilluminated imaging sensors used for \UV\ astronomy,
the depletion region (the region with significant electric field) does not 
penetrate all the way into the device.
As a result, there is a so-called field-free region near the back of the sensor
where photoelectrons must undergo a random walk to find their way to the
depletion region where they can then be conducted to the terminals and measured
\citep{Janesick2001}.
This random walk generally leads to a loss of spatial resolution measured by
the sensor since electrons can diffuse to adjacent pixels.
It also leads to an apparent reduction in the noise of a flat field measured by the sensor since
the blurring due to this diffusion induces a correlation between neighboring 
pixels.

Using Monte Carlo modeling, \citet{Janesick2001} found the following analytic
expression for the standard deviation of the charge diffusion kernel:
\begin{equation}
    \label{eq:chargeDiffusion}
    \sigma(z) = \begin{cases}
        z_f \sqrt{1 - z / z_f}, & 0 < z < z_f \\
        0, & z_f < z < D,
    \end{cases}
\end{equation} 
where $z$ is the distance from the back surface at which the photon is absorbed,
\begin{equation}
    z_f = D - z_d
\end{equation}
is the thickness of the field-free region of the sensor,
and $z_d$ is the thickness of the depletion region.
Using Equation \ref{eq:chargeDiffusion},
we can find the average variance of the charge diffusion kernel by taking an
mean across the entire thickness of the sensor weighted by the probability of
a photon being absorbed at that depth,
\begin{equation} \label{eq:chargeDiffusionWidth}
\langle\sigma^2\rangle = \frac{z_f \left( \alpha z_f + e^{-\alpha z_f} - 1 \right)}
                              {\alpha \left( 1 - e^{-\alpha D} \right)}.
\end{equation}
The thickness of the depletion region or the field-free region is difficult
to measure, and depends on the voltage applied to the sensor and the charge
collected at the terminals \citep{Stern2004}.

However, \citet{Stern2004} did measure the size of the charge diffusion kernel,
for two discrete wavelengths, of a \goesCcdThickness-thick 
(100 $\Omega$-cm resistivity) \CCD\ for the GOES Soft X-ray Imager.
We can use these measurements to estimate the size of the depletion region
and model the size of the charge diffusion kernel as a function of wavelength.
\cite{Stern2004} did not directly measure the size of the charge diffusion kernel,
instead they measured a quantity they named the \MCC, the fraction of charge
captured by the central pixel.
Naively, the \MCC\ would be the integral of the charge diffusion kernel over the
extent of a pixel.
However, since a photon can strike anywhere within the central pixel,
we need to convolve with a rectangle function the width of a pixel before
integrating.
So, our definition for the \MCC\ is
\begin{equation}
    \label{eq:mccIntegral}
    \text{MCC} = \left\{ \frac{1}{d} \int_{-d/2}^{d/2} \left[ K(x') * \Pi \left( \frac{x'}{d} \right) \right](x) \, dx \right\}^2,
\end{equation}
where $K(x)$ is the charge diffusion kernel,
$\Pi(x)$ is the rectangle function,
and $d$ is the width of a pixel.
If we assume that the charge diffusion kernel is a Gaussian with variance 
$\langle\sigma^2\rangle$, then we can analytically solve for the \MCC,
\begin{equation}
    \label{eq:mcc}
    \text{MCC} = \left[ \frac{1}{\sqrt{\pi a}} \left( e^{-a} - 1 \right) + \text{erf} \left( \sqrt{a} \right) \right]^2,
\end{equation}
where $a = d^2 / 2 \langle\sigma^2\rangle$,
and $\text{erf}(x)$ is the error function."""
    )
    subsection_charge_spreading.append(ccd_snr.figures.charge_diffusion())
    subsection_charge_spreading.append(ccd_snr.figures.diffusion_kernel())
    subsection_charge_spreading.append(
        r"""
In the top panel of Figure~\ref{fig:chargeDiffusion},
we have  plotted a fit of Equation~\ref{eq:mcc} to the measurements in 
\citet{Stern2004} which found $z_d=\depletionThickness$ best matched the data. 
The fit is qualitatively better than the models shown in \cite{Stern2004}.
In the lower panel of Figure~\ref{fig:chargeDiffusion},
we have plotted the corresponding standard deviation of the charge diffusion
kernel as a function of wavelength which predicts that the charge diffusion is
reasonably constant over much of the \SXR\ and ultraviolet wavelengths
since the penetration depth is low in this regime.

To forward model this charge diffusion in a practical way,
we've included Figure~\ref{fig:chargeDiffusionKernel},
a $3 \times 3$ kernel where the value in each pixel has been computed in
a manner similar to Equation~\ref{eq:mccIntegral},
just with different limits of integration.
We used the \IRIS\ pixel size and a representative wavelength 
to demonstrate the worst-case scenario for \IRIS.
This kernel is intended to be convolved with an input image after the noise
model (described above) has been applied to approximate the effects of charge
diffusion and complete the forward model of the sensor.
"""
    )
    result.append(subsection_charge_spreading)

    return result
