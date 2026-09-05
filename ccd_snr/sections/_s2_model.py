import aastex

__all__ = [
    "model",
]

import ccd_snr.figures


def model() -> aastex.Section:
    result = aastex.Section("Sensor Model")
    result.append(r"""
In this work, we will use the back-illuminated CCD model described in 
\citet{Stern1994} as a basis for our sensor model to make it directly comparable with 
previous works in the literature.
Figure~\ref{fig:schematic} is a schematic of our sensor model and it shows
the light-sensitive region of the sensor to be an epitaxial silicon layer with a thickness $D$.
A fraction of the incident photons are either absorbed in the oxide layer (thickness $\delta$)
or reflected at the first or second interface.
The illuminated side of the epitaxial layer is considered to have a \PCC\ region
of thickness $W$, 
where electron-hole pairs can recombine before being measured,
and there is a depletion region of thickness $z_d$ on the non-illuminated side.

In Section~\ref{subsec:Signal} we will calculate the signal predicted by this sensor
model using the method described in \citet{Stern1994}, adapted to more recent
measurements.
In Section~\ref{subsec:Noise} we will calculate the noise predicted by this sensor
model in a self-consistent manner,
and in Section~\ref{subsec:ChargeDiffusion} we will model the charge diffusion
of this sensor which is needed for a complete description of the noise.
Throughout this section we will adopt the convention that unprimed variables
represent quantities incident on the sensor,
primed variables represent quantities internal to the sensor,
and the double-primed variables represent quantities measured by the sensor.
""")
    result.append(ccd_snr.figures.schematic())
    subsection_qe = aastex.Subsection("Signal")
    subsection_qe.append(ccd_snr.figures.absorbance_and_cce())
    subsection_qe.append(ccd_snr.figures.qe_effective())
    subsection_qe.append(ccd_snr.tables.ccd_models())
    subsection_qe.append(r"""
The average number of photoelectrons measured per incident photon is known as the \QE.
This is a common performance metric for measuring sensor sensitivity and it is
given in \citet{Janesick2001} as
\begin{equation} \label{eq:quantum-efficiency}
    \text{QE}(\lambda, T) = \biggl \langle \frac{N_{e}''}{N_\gamma} \biggr \rangle
                          = A(\lambda) \, \E{n}(\lambda, T) \, \E{\eta}(\lambda),
\end{equation}
where $\lambda$ is the wavelength of the incident photons in vacuum,
$T$ is the temperature of the sensor,
$\langle X \rangle = \E{X}$ denotes the expected value of a random variable $X$,
$N_e''$ is the number of electrons measured by the sensor,
$N_\gamma$ is the total number of photons incident on the sensor,
$A(\lambda)$ is the absorbance of the light-sensitive layer, 
$\E{n}(\lambda, T)$ is the average quantum yield,
the number of photoelectrons generated per absorbed photon,
and $\E{\eta}(\lambda)$ is the average \CCE,
the fraction of generated photoelectrons measured by the sensor.

The fraction of incident energy that is absorbed by the light sensitive layer
is the absorbance, $A(\lambda)$, which is reduced by
reflections at each interface,
absorption in the oxide layer (\UV),
or by penetration through the device (\SXR\ and \IR).
$A(\lambda)$ can be determined from the optical constants of Si 
and $\text{SiO}_2$ using, for example, the popular IMD code \citep{Windt1998}.
For this work, we used our Python library, 
\href{https://optika.readthedocs.io}{\texttt{optika}} \citep{optika}, 
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

Determining $\E{n}(\lambda, T)$ over the entire wavelength range considered 
in this study is an area of ongoing research \citep[just to name a few]{Fraser1994,Geist1996,Scholze1998,Fang2019}.
This work will use the quantum yield model developed by \citet{Ramanathan2020}
which uses a phenomenological model of impact ionization to bridge the ``UV gap'',
an area where direct measurements of the quantum yield are not yet available.
They give the average quantum yield as 
\begin{equation} \label{eq:iqy}
    \E{n}(E, T) = \begin{cases}
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
is the asymptotic mean energy per electron-hole pair,
$A = \qty{5.2}{\square\electronvolt}$,
and
\begin{equation}
    E_g(T) = \qty{1.1692}{\electronvolt} - \frac{(\qty{4.9e-4}{\electronvolt\per\kelvin}) \, T^2}{T + \qty{655}{\kelvin}},
\end{equation}
is the bandgap energy of silicon.

In \citet{Stern1994}, the average \CCE\ is expressed in terms of a differential \CCE,
$\eta(z)$, which is the fraction of photoelectrons collected for a photon 
absorbed at a depth $z$ into the epitaxial layer.
The average \CCE\ is then the first moment of the differential \CCE\ weighted by 
the probability of absorbing a photon at a depth $z$,
\begin{equation} \label{cce}
    \E{\eta}(\lambda) = \frac{\int_0^\infty \eta(z) \, e^{-\alpha(\lambda) z} \, dz}
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
where $\eta_0$ is the differential \CCE\ at the back surface of the sensor.
Plugging Equation \ref{differential-cce} into Equation \ref{cce} yields an
expression for the \CCE,
\begin{equation}
    \E{\eta}(\lambda) = \eta_0 + \left( \frac{1 - \eta_0}{\alpha W} \right)(1 - e^{-\alpha W}),
\end{equation}
which can be used in Equation \ref{eq:quantum-efficiency} to determine the \QE.
In Figure \ref{fig:absorbanceAndCCE} we have plotted the average \CCE\ for
the \citet{Heymes2020} parameters in Table \ref{table:models}.

In \citet{Stern1994}, the authors define an effective \QE\ as
\begin{equation} \label{eqe}
    \text{EQE}(\lambda) = A(\lambda) \, \E{\eta}(\lambda),
\end{equation}
which is found by taking the ratio of the current measured by the sensor
to the current measured by a calibrated photodiode
and is the quantity that is typically measured when calibrating an image sensor
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
""")
    result.append(subsection_qe)

    subsection_noise = aastex.Subsection("Noise")
    subsection_noise.append(ccd_snr.figures.noise())
    subsection_noise.append(r"""
Our noise model will consider three sources:
shot noise from the quantized nature of the photons striking the sensor,
Fano noise due to inherent randomness in the process which converts photons
to electrons,
and noise due to electrons randomly recombining before they can be measured by
the sensor.
This section will describe the statistics of each noise source and demonstrate
a procedure which can simulate the noise measured by our model sensor
for a given number of incident photons.

Throughout this work, we will measure noise in terms of a \VMR,
\begin{equation}
    F(X) =  \frac{\text{Var}(X)}{\E {X}},
\end{equation}
where $\text{Var}(X)$ is the variance of $X$.
Using the \VMR\ instead of the \SNR\ to express the noise is convenient since it is constant as a 
function of signal for the distributions studied here.
For example, the \VMR\ of a Poisson random variable is always unity since its 
variance and expectation value are equal.
The \VMR\ is not dimensionless
(it has the same units as $X$),
so we must take care to interpret the \VMR\ in terms of the correct units.
For a constant multiple of a random variable, $a X$,
\begin{equation}
    F(a X) = a F(X).
\end{equation}
We will use this relationship throughout this work to convert from incident photons
to measured electrons and vice versa.

In Figure~\ref{fig:Noise} we have plotted
the \VMR\ for the noise sources considered in this study in two different units:
number of incident photons and number of measured electrons.
Figure~\ref{fig:Noise}a is useful when \textit{designing} an instrument since
the number of photons incident on the sensor can be determined by the radiance
of the source and the effective area of the instrument.
Figure~\ref{fig:Noise}b is useful when \textit{calibrating} an instrument
since we directly measure these electrons.
The details of the calculations for Figure~\ref{fig:Noise} are presented in the 
subsections below.
""")
    subsubsection_noise_shot = aastex.Subsubsection("Shot Noise")
    subsubsection_noise_shot.append(r"""
Photon shot noise is often assumed to be the leading 
noise contributor in \UV\ astronomy \citep{Stern1986,Lemen2012,DePontieu2014}.
If the expected number of photons that interact with the light-sensitive layer is
\begin{equation}
    \E{N}_\gamma'  = A \E{N}_\gamma.
\end{equation}
then the actual number of interacting photons,
$N_\gamma'$, 
is sampled from the Poisson distribution,
\begin{equation} \label{eq:shot-noise-variance}
    N_\gamma' \leftarrow \text{Poisson} \bigl( \E{N}_\gamma' \bigr).
\end{equation}
As mentioned in the previous section,
the \VMR\ of this process is
\begin{equation} \label{eq:absorbed-photon-vmr}
    F(N_\gamma') = 1, 
\end{equation}
but this in terms of the number of absorbed photons, which is internal to the sensor.
In terms of the expected number of incident photons given the number of absorbed photons
the \VMR\ is
\begin{equation} \label{eq:photonShotFano}
    F_{\gamma,\text{shot}} \equiv F \left(\frac{N_\gamma'}{A} \right) = \frac{1}{A}
\end{equation}
since $A$ is the conversion factor between incident photons and absorbed photons.
$F_{\gamma,\text{shot}}$ is plotted in Figure~\ref{fig:Noise}a in blue and demonstrates
that this expression is nearly unity across almost the entire wavelength
range of the sensor except in the \UV, where the absorbance is poor
(Figure~\ref{fig:absorbanceAndCCE}).
We can also express the \VMR\ of the shot noise in terms of the
number of measured electrons by using the \QE\ as the conversion factor between
the unprimed and double-primed variables,
\begin{equation} \label{eq:electronShotVmr}
    F_{e,\text{shot}}'' = \E{n} \, \E{\eta}.
\end{equation}
This equation is plotted in Figure~\ref{fig:Noise}b in blue,
where we can see that it increases linearly with decreasing wavelength since
the average quantum yield is increasing.
""")
    subsection_noise.append(subsubsection_noise_shot)
    subsubsection_noise_fano = aastex.Subsubsection("Fano Noise")
    subsubsection_noise_fano.append(r"""
The energy resolution of silicon detectors is ultimately limited due to Fano
noise \citep{Fano1947}, the random variation of the quantum yield $n$.
Fano noise is usually expressed in terms of the Fano factor, 
$\mathcal{F} = F(n)$.
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
is a Gaussian distribution centered around $\E{n}(\lambda, T)$,
with standard deviation $\sqrt{\E{n}(\lambda, T) \, \mathcal{F}(T)}$,
where $\mathcal{F}(T)$ is the asymptotic Fano factor given by \citet{Ramanathan2020} as
\begin{equation}
    \mathcal{F}(T) = (\qty{-0.028}{\per\electronvolt}) \, E_g(T) + (\qty{0.0015}{\per\square\electronvolt}) \, A + 0.14.
\end{equation}
At \qty{300}{K}, this corresponds to a Fano factor of approximately 0.114,
which is generally consistent with the best-available measurement of the
Fano factor by \citet{Rodrigues2021} at \SI{6}{\kilo\electronvolt}.

$\mathcal{F}$ is a quantity internal to the sensor.
The measured Fano factor is instead
\begin{equation}
    F_{e,\text{Fano}}'' = \E{\eta} \mathcal{F}
\end{equation}
since the conversion factor between the generated electrons and the measured
electrons is the \CCE. 
In Figure~\ref{fig:Noise}b we have plotted $F_{e,\text{Fano}}''$ in green.
This shows that the Fano noise is the smallest contributor to the total noise
across the entire wavelength range and is often at least an order of magnitude
smaller than the other noise sources.
""")
    subsection_noise.append(subsubsection_noise_fano)
    subsubsection_noise_recombination = aastex.Subsubsection(
        "Partial Charge Collection Noise",
    )
    subsection_noise.append(ccd_snr.figures.penetration_depth())
    subsection_noise.append(ccd_snr.figures.energy_spectrum())
    subsubsection_noise_recombination.append(r"""
In Figure~\ref{fig:penetrationDepth}, we have plotted the penetration depth in
silicon vs. the thickness of the \PCC\ region.
We can see that there are two regions in the \UV\ where the penetration depth
is less than the thickness of the \PCC\ region.
In these regions, there is a significant chance that some of the electron-hole pairs
will randomly recombine before being measured by the sensor.
The stochastic nature of this process leads us to consider this as a new noise
source, \PCC\ noise.

In the \citet{Stern1994} charge-collection model, 
each photoelectron generated in the \PCC\ region has a probability 
$\eta(z)$ of \textit{not} recombining and subsequently being measured 
by the sensor.
If $n_i'$ is the quantum yield of the $i$th photon generated using
the \citet{Ramanathan2020} model discussed in the previous section,
we can express the \textit{measured} quantum yield as
\begin{equation} \label{eq:measuredQuantumYield}
    n_i'' \leftarrow \text{Binomial}\bigl(n_i', \eta(z_i) \bigr),
\end{equation}
where
$z_i$ is the penetration depth of the $i$th photon
and $\text{Binomial}(n, p)$ is a sample from the binomial distribution
with $n$ trials and probability of success $p$.
We can use \ref{eq:measuredQuantumYield} to compute the total number of measured
electrons given $N_\gamma'$ absorbed photons as
\begin{equation} \label{eq:measuredElectrons}
    N_e'' = \sum_{i=0}^{N_\gamma'} n_i''.
\end{equation}
This expression is intended to be used in an instrument forward model to sample 
the distribution of measured electrons given an expected number of incident photons.

At first glance the \VMR\ of this process looks intractable,
since Equation~\ref{eq:measuredElectrons} is a sum of binomial draws in which
both the number of trials and the probability of success vary from one term to
the next.
It is made tractable by the observation made at the start of this section,
that the \VMR\ is constant as a function of signal,
which leaves us free to evaluate it at whichever illumination is most
convenient.
The most convenient is the faintest.
Consider an exposure so brief that the entire pixel array receives a single
photon with probability $\varepsilon$ and no photon at all otherwise.
Let $X$ be the number of electrons collected by a given pixel,
and $X_1$ the number that same pixel collects on those occasions when the photon
is present.
The empty exposures contribute nothing to either average, so
\begin{equation} \label{eq:faintMoments}
    \E{X} = \varepsilon \, \E{X_1},
    \qquad
    \E{X^2} = \varepsilon \, \E{X_1^2},
\end{equation}
and the \VMR\ of the exposure is
\begin{equation} \label{eq:faintVmr}
    F(X) = \frac{\E{X^2} - \E{X}^2}{\E{X}}
         = \frac{\E{X_1^2}}{\E{X_1}} - \varepsilon \, \E{X_1} .
\end{equation}
As the exposure is made fainter the second term vanishes,
and the \VMR\ is fixed entirely by the first two moments of what a single photon
delivers to a single pixel.
Since the \VMR\ does not depend on the illumination,
this limit is the answer at any illumination.

In this subsection charge diffusion is neglected,
so the electrons liberated by that photon are all collected by the pixel it
struck, and $X_1$ is simply the measured quantum yield $n''$.
Both of its moments follow from Equation~\ref{eq:measuredQuantumYield}.
For a photon which liberates $n'$ electrons at a depth $z$,
the measured yield $n''$ is binomial,
with mean $n' \eta(z)$ and variance $n' \eta(z) \bigl( 1 - \eta(z) \bigr)$,
so its second moment is
\begin{equation} \label{eq:secondMomentConditional}
    \E{(n'')^2} \big|_{n', z} = n' \eta (1 - \eta) + \bigl( n' \eta \bigr)^2 .
\end{equation}
Averaging over the absorption depth and the quantum yield,
which are independent at a given wavelength,
and using $\text{Var}(n') = \mathcal{F} \E{n}$ to evaluate $\E{(n')^2}$,
gives
\begin{equation} \label{eq:secondMoment}
    \E{(n'')^2} = \E{n} \, \E{\eta}
                + \E{n} \bigl( \E{n} + \mathcal{F} - 1 \bigr) \E{\eta^2} .
\end{equation}
The mean is simply $\E{n''} = \E{n} \, \E{\eta}$,
so dividing Equation~\ref{eq:secondMoment} by it gives the \VMR\ of the electrons
measured by the sensor,
\begin{equation} \label{eq:totalVmr}
    F_e'' = 1 + \bigl( \E{n} + \mathcal{F} - 1 \bigr) \frac{\E{\eta^2}}{\E{\eta}} .
\end{equation}

The two terms of Equation~\ref{eq:secondMoment} are worth distinguishing,
since they respond differently to charge diffusion in
Section~\ref{subsec:ChargeDiffusion}.
Each factor of $\eta$ is the probability that one electron survives
recombination, so the number of factors counts the electrons a term describes.
The first term carries a single factor and is the contribution of the electrons
taken one at a time;
it becomes the leading unity of Equation~\ref{eq:totalVmr},
which is why the \VMR\ measured in electrons can never fall below one.
The second term carries two factors, through $\E{\eta^2}$,
and describes the electrons two at a time.
It is nonzero only because a single photon can liberate more than one electron,
and it is the entire excess above the Poisson floor.

It is conventional to express this result in terms of the \VMR\ of the \CCE\
rather than its second moment.
Taking the second moment of Equation~\ref{differential-cce} in a similar fashion
to Equation~\ref{cce} gives
\begin{equation}
    F(\eta) = \frac{2 e^{-\alpha W}}{\E{\eta}} \left( \frac{1 - \eta_0}{\alpha W} \right)^2 \bigl( \sinh(\alpha W) - \alpha W \bigr),
\end{equation}
and rearranging the definition of the \VMR\ shows that the ratio appearing in
Equation~\ref{eq:totalVmr} is simply $\E{\eta} + F(\eta)$.
Substituting this and setting aside the shot noise of
Equation~\ref{eq:electronShotVmr} leaves the combined Fano and \PCC\
contribution,
\begin{equation} \label{eq:sensorVmr}
    F_{e,\text{sensor}}'' = F_e'' - F_{e,\text{shot}}''
        = 1 + (\mathcal{F} - 1) \E{\eta} + \bigl( \E{n} + \mathcal{F} - 1 \bigr) F(\eta).
\end{equation}
The contribution from only PCC noise is then
\begin{equation}
    F_{e,\text{PCC}}'' = F_{e,\text{sensor}}'' - F_{e,\text{Fano}}'',
\end{equation}
which is plotted in Figure~\ref{fig:Noise} in orange.
We can see that the \PCC\ noise is usually very small compared to the shot noise,
but in the \UV\,
from about \qtyrange{2000}{3500}{\angstrom},
it actually exceeds the shot noise and is the dominant contributor to the noise.

In Figure~\ref{fig:energySpectrum},
we have plotted the \PMFs\ of Equation~\ref{eq:measuredElectrons} and the
\citet{Stern1986} noise model to visualize the differences between these two
distributions.
Each model has been evaluated on a grid where each column of the grid represents
a different wavelength
(chosen to demonstrate the worst-case differences between the two models)
and each row represents a different expected number of
absorbed photons.
When the number of absorbed photons is low,
like in the bottom two rows of Figure~\ref{fig:energySpectrum},
we can see that the \citet{Stern1986} model (orange) has a comb-like appearance
caused by the Fano noise slightly blurring the \PMF\ of the photon shot noise.
In contrast, our model shows much less of this comb pattern since the \PCC\
noise tends to blur the distribution further into a single peak.
As the number of photons increases,
both distributions tend towards a Gaussian,
but our model remains narrower.

To ease adoption of this model,
we've provided a reference implementation of Equation~\ref{eq:measuredElectrons}
in Python,
\href{https://optika.readthedocs.io/en/latest/_autosummary/optika.sensors.signal.html}{\texttt{optika.sensors.signal()}},
which is designed to be simple to use for existing and future instrument pipelines.
""")
    subsection_noise.append(subsubsection_noise_recombination)
    result.append(subsection_noise)

    subsection_charge_spreading = aastex.Subsection("Charge Diffusion")
    subsection_charge_spreading.append(r"""
In most back-illuminated imaging sensors used for \UV\ astronomy,
the depletion region (the region with significant electric field) does not 
extend all the way from the gate structure through the device.
As a result, there is a so-called field-free region near the back of the sensor
where photoelectrons must undergo a random walk to find their way to the
depletion region where they can then be conducted to the terminals and measured
\citep{Janesick2001}.
This random walk generally leads to a loss of spatial resolution measured by
the sensor since electrons can diffuse to adjacent pixels.
It can also lead to a reduction in the variance of a flat field measured by the
sensor, but only where a single photon liberates more than one electron.
The random walk displaces each electron independently of every other,
so for a quantum yield of unity it carries one Poisson distribution of electrons
into another and leaves the variance of a flat field unchanged.
Where the quantum yield exceeds unity, the electrons liberated by a single
photon would otherwise be collected together,
and spreading them across neighboring pixels both reduces the variance and
induces a covariance between those pixels.

Using Monte Carlo modeling, \citet{Janesick2001} found the following
expression for the standard deviation of the charge diffusion kernel:
\begin{equation}
    \label{eq:chargeDiffusion}
    \sigma(z) = \begin{cases}
        z_f \sqrt{1 - z / z_f}, & 0 < z < z_f \\
        0, & z_f < z < D,
    \end{cases}
\end{equation} 
where $z$ is the distance from the back surface at which the photon is absorbed,
$z_f = D - z_d$ is the thickness of the field-free region of the sensor,
and $z_d$ is the thickness of the depletion region.
Using Equation \ref{eq:chargeDiffusion},
we can find the average variance of the charge diffusion kernel by taking a
mean across the entire thickness of the sensor weighted by the probability of
a photon being absorbed at that depth,
\begin{equation} \label{eq:chargeDiffusionWidth}
\E{\sigma^2} = \frac{z_f \left( \alpha z_f + e^{-\alpha z_f} - 1 \right)}
                              {\alpha \left( 1 - e^{-\alpha D} \right)}.
\end{equation}
The thickness of the depletion region or the field-free region is difficult
to measure, and depends on the voltage applied to the sensor and the charge
collected at the terminals \citep{Stern2004}.

However, \citet{Stern2004} did estimate the size of the charge diffusion kernel,
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
If we assume that the charge diffusion kernel is a Gaussian with variance $\E{\sigma^2}$,
then the \MCC\ is
\begin{equation}
    \label{eq:mcc}
    m = \left[ \frac{1}{\sqrt{\pi a}} \left( e^{-a} - 1 \right) + \text{erf} \left( \sqrt{a} \right) \right]^2,
\end{equation}
where $a = d^2 / 2 \E{\sigma^2}$,
$d$ is the width of a pixel, 
and $\text{erf}(x)$ is the error function.""")
    subsection_charge_spreading.append(ccd_snr.figures.charge_diffusion())
    subsection_charge_spreading.append(ccd_snr.figures.diffusion_kernel())
    subsection_charge_spreading.append(r"""
In the top panel of Figure~\ref{fig:chargeDiffusion},
we have  plotted a fit of Equation~\ref{eq:mcc} to the measurements in 
\citet{Stern2004} which found $z_d=\depletionThickness$ best matched the data. 
In the lower panel of Figure~\ref{fig:chargeDiffusion},
we have plotted the corresponding standard deviation of the charge diffusion
kernel as a function of wavelength which predicts that the charge diffusion is
reasonably constant over much of the \SXR\ and ultraviolet wavelengths
since the penetration depth is low in this regime.
Since the depletion thickness depends on the resistivity and bias voltage of
a particular device, in Appendix~\ref{appendix:tracks} we check this model
against the charge diffusion measured directly on the \IRIS\ \CCDs\ using the
tracks left by energetic particles.
The probability that two electrons liberated at the back surface are collected
in the same pixel, which is the quantity that enters our noise model below,
is $\sjiSamePixel \pm \sjiSamePixelError$ on the \IRIS\ \SJI\ \CCD,
compared to \sjiSamePixelModel\ predicted by this model.

To visualize the extent of this charge diffusion,
we've included Figure~\ref{fig:chargeDiffusionKernel},
a $3 \times 3$ kernel where the value in each pixel has been computed in
a manner similar to Equation~\ref{eq:mcc},
just with different limits of integration.
We used the \IRIS\ pixel size and a representative wavelength
to demonstrate the worst-case scenario for \IRIS.
Convolving this kernel with an image approximates the spatial extent of the
charge diffusion, but it does not describe the process faithfully.
A convolution assigns a fractional number of electrons to each pixel, whereas
every electron is in fact collected by exactly one pixel, and it treats the
displacement of each electron as independent, whereas the electrons liberated
by a single photon share both an absorption depth and a sub-pixel origin.
We therefore diffuse each electron individually, displacing it by
$\mathcal{N}\bigl(0, \sigma^2(z_i)\bigr)$ in each direction and rounding to the
nearest pixel, which conserves charge exactly and preserves the correlation
between electrons from the same photon.
This is implemented by
\href{https://optika.readthedocs.io/en/latest/_autosummary/optika.sensors.signal.html}{\texttt{optika.sensors.signal()}},
and the kernel in Figure~\ref{fig:chargeDiffusionKernel} was computed with
\href{https://optika.readthedocs.io/en/latest/_autosummary/optika.sensors.kernel\_diffusion.html}{\texttt{optika.sensors.kernel\_diffusion()}},
which can be used to visualize the charge diffusion for other wavelengths and
pixel sizes.

Charge diffusion does not add a noise source of its own.
It moves electrons between pixels without creating or destroying any, so it
leaves the mean of a flat-field image unchanged, and it reduces the variance
only by weakening the correlation between electrons that came from the same
photon.
To find its effect on the noise we return to the faint exposure of
Section~\ref{subsec:Noise}, in which the array receives at most one photon.
The image is then nothing but the charge liberated by that photon,
and the only thing diffusion changes is how it is divided between the pixels,
so we now ask how many of the photon's electrons each \textit{pixel} collects
rather than how many survive in total.
Let $m$ be the number of electrons which survive recombination,
as in Section~\ref{subsec:Noise},
and let $q_j$ be the probability that any one of \textit{those} electrons is
collected by pixel $j$.
Recombination has therefore already been accounted for in $m$,
and $q_j$ describes only where the surviving charge is delivered,
so that $\sum_j q_j = 1$;
the \CCE\ enters this section through $m$ and not through $q_j$.
The electrons are displaced independently of one another,
so the photon contributes
$X_j \leftarrow \text{Binomial}(m, q_j)$ to pixel $j$,
and the second moment summed over the pixels is
\begin{equation} \label{eq:diffusedSecondMoment}
    \sum_j \E{X_j^2} = m \sum_j q_j - m \sum_j q_j^2 + m^2 \sum_j q_j^2
                     = m + m (m - 1) \sum_j q_j^2 .
\end{equation}
Two quantities have appeared which were not present in
Section~\ref{subsec:Noise}.
The sum $\sum_j q_j^2$ is the probability that two electrons displaced
independently are collected by the same pixel,
and the factor $m(m-1)$ multiplying it is the number of ordered pairs of
distinct electrons the photon delivered.
Neither was introduced by hand.
Both are produced by the algebra, and they arrive together,
because the only way that spreading the charge can alter the second moment is by
separating electrons which would otherwise have been counted in the same pixel.
Where no charge is shared, $\sum_j q_j^2 = 1$,
Equation~\ref{eq:diffusedSecondMoment} collapses to $m^2$,
and the result of Section~\ref{subsec:Noise} is recovered;
this is why the pairs are invisible there and unavoidable here.
The opposite extreme is equally simple.
Where the charge is spread so widely that no two electrons share a pixel,
$\sum_j q_j^2$ falls to zero and the sum of squares collapses to $m$,
which is to say the image becomes a set of electrons bearing no relation to one
another and the \VMR\ falls to unity.
Between these limits the \VMR\ measured in electrons is nothing more than the
ratio of the sum of the squares of a single-photon image to the sum of that same
image, and charge diffusion moves it from one end of that range to the other.

It remains to evaluate $\sum_j q_j^2$ for the charge diffusion described by
Equation~\ref{eq:chargeDiffusion}.
Two electrons liberated by the same photon begin their random walks from a
common absorption depth and a common position within a pixel,
so how often they are collected together depends on how far the charge spreads
at the depth where the photon was absorbed,
expressed in units of the pixel width,
\begin{equation} \label{eq:probabilitySamePixel}
\begin{split}
    \mathcal{P}(z) &= p\bigl(\sigma(z) / d\bigr)^2, \\
    p(s) &= \text{erf}\left( \frac{1}{2 s} \right)
            - \frac{2 s}{\sqrt{\pi}} \left( 1 - e^{-1 / 4 s^2} \right),
\end{split}
\end{equation}
where $\mathcal{P}(z)$ is $\sum_j q_j^2$ averaged over the position of the photon
within its pixel,
$p(s)$ is the corresponding probability for a single axis,
$d$ is the width of a pixel,
and the square accounts for the two directions across the face of the sensor,
which spread independently of one another.
In the limit of a narrow charge cloud this probability approaches unity and the
electrons remain together;
in the opposite limit it falls to zero and they are scattered independently.

Averaging Equation~\ref{eq:diffusedSecondMoment} over the quantum yield and the
absorption depth, exactly as in Section~\ref{subsec:Noise},
requires $\E{m} = \E{n} \, \E{\eta}$ as before,
and $\E{m(m-1)} = \E{n} \bigl( \E{n} + \mathcal{F} - 1 \bigr) \E{\eta^2}$,
since a pair survives recombination only if both of its electrons do.
Dividing by the mean gives the \VMR\ measured by a sensor with charge diffusion,
\begin{equation} \label{eq:diffusedVmr}
    F_{e,\text{diff}}'' = 1 + \bigl( \E{n} + \mathcal{F} - 1 \bigr)
        \frac{\E{\mathcal{P} \eta^2}}{\E{\eta}}.
\end{equation}
Comparing with Equation~\ref{eq:totalVmr},
the effect of charge diffusion is to discount the two-electron term by the
probability that the two electrons are in fact measured together,
and to leave the one-electron term untouched.
The discount is applied inside the average over absorption depth rather than
outside it, since the distance the charge spreads and the fraction of it that
survives recombination both depend on where in the sensor the photon was
absorbed, and the two are correlated:
photons absorbed near the back surface are the ones which both recombine most
readily and diffuse the furthest.
Equation~\ref{eq:diffusedVmr} is the form implemented by
\href{https://optika.readthedocs.io/en/latest/_autosummary/optika.sensors.vmr_signal.html}{\texttt{optika.sensors.vmr\_signal()}}
and plotted for \IRIS\ in Figure~\ref{fig:Noise}.
It assumes the illumination is uniform, so that the charge leaving each pixel is
balanced on average by the charge arriving from its neighbors;
near the edge of the sensor, where diffused charge is lost, it is an
approximation.
""")
    result.append(subsection_charge_spreading)

    return result
