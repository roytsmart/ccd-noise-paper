import aastex

__all__ = [
    "model",
]

import ccd_snr.figures


def model() -> aastex.Section:
    result = aastex.Section("CCD Model")
    result.append(ccd_snr.figures.qe_effective())
    result.append(ccd_snr.tables.models())
    result.append(
        r"""
In this work, we will model the light-sensitive region of the backilluminated 
sensor as a epitaxial silicon layer with a thickness $D$, which is coated
with a thin oxide layer of thickness $\delta$ to provide a realistic transmission 
coefficient.
The illuminated side of the epitaxial layer is considered to have a \PCC\ region
of width $W$, where some of the generated photoelectrons recombine before being
measured by the sensor.
\PCC\ is usually described by quantity called \CCE, the fraction of 
photoelectrons which do \textit{not} recombine and are measured by the sensor.
In Section \ref{subsec:Noise} we will see how \PCC\
affects the variance of the signal measured by an imaging sensor.
"""
    )
    subsection_qe = aastex.Subsection("Quantum Efficiency")
    subsection_qe.append(
        r"""
\QE\ is the average number of photoelectrons measured per photon and is a common 
performance metric for measuring sensor sensitivity.
It is given in \citet{Janesick2001} as
\begin{equation} \label{quantum-efficiency}
    \text{QE}(\lambda) = \frac{N_{e}}{N_\gamma}
                       = A(\lambda) \times \text{IQY}(\lambda) \times \text{CCE}(\lambda),
\end{equation}
where $N_e$ is the number of electrons measured by the sensor for a 
given wavelength $\lambda$,
$N_\gamma$ is the total number of photons incident on the sensor,
$A(\lambda)$ is the fraction of incident energy absorbed by the epitaxial layer, 
and $\text{IQY}(\lambda)$ is the ideal \QY, the number of photoelectrons generated 
per absorbed photon.

The absorbance $A(\lambda)$ can be determined from the optical constants of Si 
and $\text{SiO}_2$, using, for example, the popular IMD code \citep{Windt1998}.
For this work, we used our Python library, 
\texttt{optika} \citep{optika}, 
which uses the transfer matrix method described in \citet{Yeh1988} 
with the optical constants from \citet{Palik1997}, \citet{Henke1993}, and 
\citet{Rodriguez-deMarcos2016} to compute the electric field for every interface
in the sensor.
In Figure \ref{fig:absorbanceAndCCE} we've plotted $A(\lambda)$ for the 
\cite{Heymes2020} parameters in Table \ref{table:models}.

In \citet{Stern1994}, the authors assume no reflections from the unilluminated
side of the sensor for simplicity.
In this work, we compute the total change in Poynting flux into and out of the 
light-sensitive region of the sensor to determine $A(\lambda)$.
This treatment introduces interference effects for infrared wavelengths, 
which can be seen on the right side of Figure \ref{fig:absorbanceAndCCE}.

The ideal \QY\ is given by \citet{Janesick2001} as
\begin{equation}
    \text{IQY}(\lambda) = \begin{cases}
        0, & 0 < \epsilon < E_\text{g} \\
        1, & E_\text{g} < \epsilon < E_\text{eh} \\
        \epsilon / E_\text{eh}, & E_\text{eh} < \epsilon < \infty,
    \end{cases}
\end{equation}
where $\epsilon$ is the energy of an incident photon, 
$E_\text{g} = \bandgapEnergy$ is the bandgap energy of silicon,
and $E_\text{eh} = \electronHoleEnergy$ is the energy required to generate one
electron-hole pair at room temperature.
Surprisingly, despite initial results to the contrary \citep{Fraser1994},
this simple relation is a good approximation across the entire wavelength range
considered \citep{Geist1996,Scholze1998,Fang2019}.

In \citet{Stern1994}, the \CCE\ is expressed in terms of a differential \CCE,
$\eta(z)$, which is the fraction of photoelectrons collected for a photon 
absorbed at a depth $z$ into the epitaxial layer.
The total \CCE\ is then the average differential \CCE\ weighted by 
the probability of absorbing a photon at a depth $z$,
\begin{equation} \label{cce}
    \text{CCE}(\lambda) = \frac{\int_0^\infty \eta(z) \exp(-\alpha z) \, dz}
                               {\int_0^\infty \exp(-\alpha z) \, dz},
\end{equation}
where $\alpha$ is the absorption coefficient of silicon for the given wavelength.

In principle, $\eta(z)$ is a function of the exact implant profile which is
usually impractical to measure, but see \cite{Stern2004,Boerner2012} for a case 
where the authors did have a measurement of the exact implant profile provided 
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
arithmetic expression for the \CCE,
\begin{equation}
    \text{CCE}(\lambda) = \eta_0 + \left( \frac{1 - \eta_0}{\alpha W} \right)(1 - e^{-\alpha W}),
\end{equation}
which can be used in Equation \ref{quantum-efficiency} to determine the \QE.
In Figure \ref{fig:absorbanceAndCCE} we've plotted $\text{CCE}(\lambda)$ for
the \citet{Heymes2020} parameters in Table \ref{table:models}.

In \citet{Stern1994}, the authors define an effective \QE\ as
\begin{equation} \label{eqe}
    \text{EQE}(\lambda) = A(\lambda) \times \text{CCE}(\lambda),
\end{equation}
which is the quantity that is typically measured when calibrating a image sensor
\citep{Stern1994,Stern2004,Boerner2012}.
In Figure~\ref{fig:eqe}, we've plotted the measured, effective \QE\ for two
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
    subsection_qe.append(ccd_snr.figures.absorbance_and_cce())
    result.append(subsection_qe)

    subsection_noise = aastex.Subsection("Noise")
    subsection_noise.append(ccd_snr.figures.noise_photon())
    subsection_noise.append(ccd_snr.figures.noise_electron())
    result.append(ccd_snr.tables.fano_factor())
    subsection_noise.append(
        r"""
Our noise model will consider three sources:
shot noise from the random arrival time of the photons striking the sensor,
Fano noise due to inherent randomness in the process which converts photons
to electrons,
and noise due to electrons randomly recombining before they can be measured by
the sensor.
This section will describe the statistics of each noise source and demonstrate
a simple algorithm which can simulate the noise measured by our model sensor
for a given number of incident photons.

Throughout this work, we will measure noise in terms of a \VSR,
\begin{equation}
    \text{VSR}(X) = \frac{\text{Var}(X)}{\langle X \rangle},
\end{equation}
where $X$ is a random variable,
$\text{Var}()$ is the variance of the random variable,
and $\langle \cdot \rangle$ denotes an expectation value.
Using the \VSR\ to express the noise is convenient since it's constant as a 
function of signal for most of the distributions studied here.
For example, the \VSR\ of a Poisson process is always unity since its variance and
expectation value are equal.
A disadvantage of the \VSR\ is that it is not dimensionless 
(it has the same units as $X$),
so we must take care to interpret the \VSR\ in terms of the correct units.

In Figures~\ref{fig:photonNoise}~and~\ref{fig:electronNoise} we've plotted
the \VSR\ for the noise sources considered in this study in two different units:
number of incident photons and number of measured electrons.
Figure~\ref{fig:photonNoise} is useful if you're \textit{engineering} an instrument since
you presumably know the radiance of the source and the effective area of the
rest of your instrument, and you want to know how much noise to expect in
terms of the number of photons incident on the sensor.
Figure~\ref{fig:electronNoise} is useful if you're \textit{using} an instrument
and want to know how much noise to expect for a given number of measured
electrons.
"""
    )
    subsubsection_noise_shot = aastex.Subsubsection("Shot Noise")
    subsubsection_noise_shot.append(
        r"""
Shot noise is often the leading noise contributor in \UV\ solar astronomy 
\citep{Lemen2012, DePontieu2014}.
The shot noise is described by a Poisson distribution with variance
\begin{equation} \label{eq:shot-noise-variance}
    \langle N_\gamma' \rangle = A(\lambda) \langle N_\gamma \rangle,
\end{equation}
where $\langle N_\gamma \rangle$ is the expected number of incident photons.
and $\langle N_\gamma' \rangle$ is the expected number of photons absorbed
by the light-sensitive layer.

In Figures~\ref{fig:photonNoise}~and~\ref{fig:electronNoise}
we've plotted the \VSR\ of the shot noise in blue.
In Figure~\ref{fig:photonNoise}, we can see that the \VSR\ of the shot noise
relative to the number of incident photons is often unity since it is a Poisson
process.
It deviates from unity in the \UV\ since the sensor absorbs only a fraction
of the incident light leading to more noise for a given number of incident photons.
"""
    )
    subsection_noise.append(subsubsection_noise_shot)
    subsubsection_noise_fano = aastex.Subsubsection("Fano Noise")
    subsubsection_noise_fano.append(
        r"""
The energy resolution of silicon detectors is ultimately limited due to Fano
noise \citep{Fano1947}, the unpredictable variation of the ideal \QY.
Fano noise is usually expressed in terms of the Fano factor, 
$\mathcal{F} = \sigma^2 / \mu$,
the ratio of the variance to the mean of some random process 
(very similar to our definition of \VSR\ above).

The Fano noise for silicon is commonly accepted to have a Fano factor of about 
$\mathcal{F} \approx 0.1$ \citep{Janesick2001}.
In part due to variations of the Fano noise as a function of wavelength and
temperature \citep{Fraser1994}, 
there is some disagreement in the literature around a more precise value for
$\mathcal{F}$ 
\citep[\& references therein]{Fraser1994,Lowe1997,Mazziotta2008,Kotov2018,Rodrigues2021,Rodrigues2023}.
$\mathcal{F}$ is often measured in the soft X-ray region,
traditionally with $^{55}$Fe sources, which have a high \QY.
For \UV\ wavelengths, where the \QY\ is near unity, it becomes impossible
to construct a distribution narrow enough to be consistent with a Fano factor 
that small.
Because this distribution does not exist,
and because $\mathcal{F}$ is so small compared to the other noise sources
considered in this study, 
we have decided to ignore the wavelength variation of $\mathcal{F}$,
and adopt a Fano noise model with constant $\mathcal{F} = \fanoFactor$,
which represents the best available measurement of $\mathcal{F}$ using $^{55}$Fe
X-rays \citep{Rodrigues2021}, and uses a skipper CCD \citep{Janesick1990} to 
minimize the effect of readout noise.

At high energies, Fano noise is well-described by a Gaussian distribution
\citep{Rodrigues2023}.
At low energies, a Gaussian distribution is problematic since it becomes likely
that it will be negative for some samples, which is unphsyical.
For this work, we will use a scaled Poisson distribution to describe the
the Fano noise,
\begin{equation} \label{eq:scaled-poisson}
    \langle\text{QY}\rangle \sim \text{Pois}(\text{IQY}(\lambda) / \mathcal{F}) \times \mathcal{F},
\end{equation}
where $\langle\text{QY}\rangle$ is the expected quantum yield,
and $\text{Pois}(x)$ is a sample from the Poisson distribution.
Equation \ref{eq:scaled-poisson} has the nice property of reproducing a Gaussian 
with the correct width at high energies while also being well-behaved around
$\text{IQY}(\lambda) \approx 1$.

Unfortunately, Equation \ref{eq:scaled-poisson} does not yield an integer number of electrons,
and as a last step we must randomly choose a nearby whole number in such a way 
that the mean of the distribution is unchanged. 
In this work, we used the simplest possible resolution to this problem
by defining the \PMF\
\begin{equation} \label{eq:discretization}
    P(\text{QY} = k) = \begin{cases}
        \langle\text{QY}\rangle - \lfloor \langle\text{QY}\rangle \rfloor, & k = \lfloor \langle\text{QY}\rangle \rfloor \\
        \lceil \langle\text{QY}\rangle \rceil - \langle\text{QY}\rangle, & k = \lceil \langle\text{QY}\rangle \rceil,
    \end{cases}
\end{equation}
where $\text{QY}$ is the actual quantum yield,
$\lfloor \cdot \rfloor$ denotes the floor function,
and $\lceil \cdot \rceil$ denotes the ceiling function.
Equation \ref{eq:discretization} is a choice between the two closest integers 
with the probabilities weighted to conserve the mean of the distribution.
One consequence of this \PMF\ is that it increases the apparent Fano noise
if $\langle \text{QY} \rangle$ is near unity due to discretization noise.
This apparent increase in Fano noise for low \QY\ is not unprecedented and may
explain the sawtooth variations in the Fano noise observed by \citet{Santos1991}.

In Figures \ref{fig:photonNoise} and \ref{fig:electronNoise} we can see the 
contribution of Fano noise to the total noise measured by our simulated sensor.
Note how the Fano noise component is very small compared to the photon shot noise.
"""
    )
    subsection_noise.append(subsubsection_noise_fano)
    subsubsection_noise_recombination = aastex.Subsubsection("Recombination Noise")
    subsubsection_noise_recombination.append(
        r"""
Recombination of photoelectrons in the \PCC\ region is a significant source of noise in
the \UV\ since the photons are absorbed so close to the surface,
where the \CCE\ is relatively low (Figure \ref{fig:absorbanceAndCCE}).
The probability of measuring electrons generated in the \PCC\ region is
described by a binomial distribution,
\begin{equation} \label{eq:recombination}
    \text{MQY} \sim \text{B}(\text{QY}, \text{CCE}(\lambda))
\end{equation}
where $\text{MQY}$ is the measured quantum yield,
and $\text{B}(n, p)$ is a sample from the binomial distribution.

In Figures \ref{fig:photonNoise} and \ref{fig:electronNoise} we can see that the
recombination noise is the dominant source of noise measured by the sensor
in the near/far \UV\ and remains non-negligible into the \EUV.
"""
    )
    subsection_noise.append(subsubsection_noise_recombination)
    subsubsection_algorithm = aastex.Subsubsection("Sampling Algorithm")
    subsubsection_algorithm.packages.append(
        aastex.Package(name="algorithm2e", options="ruled"),
    )
    subsubsection_algorithm.append(
        r"""
Equations \ref{eq:scaled-poisson}, \ref{eq:discretization}, and \ref{eq:recombination}
are written in terms of a single photon being absorbed by the sensor.
What would be more useful for forward modeling is a way to draw samples from the 
distribution of the number of measured electrons for a given number of expected 
incident photons without needing to simulate every photon individually.
Since the sum of $n$ independent Poisson distributions is another Poisson
distribution and similarly for $n$ independent binomial distributions with
the same probability,
we can approximate Equations \ref{eq:shot-noise-variance}-\ref{eq:recombination} in
terms of Numpy-like idioms using Algorithm \ref{alg:electron-sample},
\begin{algorithm}
\caption{
A procedure to sample the distribution of the number of measured electrons
given an expected number of incident photons.
}
\label{alg:electron-sample}
    \DontPrintSemicolon
    $\langle N_\gamma' \rangle \gets A(\lambda) \times \langle N_\gamma \rangle$\;
    $N_\gamma' \gets \texttt{poisson}(\langle N_\gamma' \rangle)$\;
    $\langle N_e \rangle \gets \text{IQY}(\lambda) \times N_\gamma'$\;
    $\langle N_e' \rangle \gets \texttt{poisson}(\langle N_e \rangle / \mathcal{F}) \times \mathcal{F}$\;
    $N_e' \gets \lfloor \langle N_e' \rangle \rfloor + \left[ \texttt{uniform}(0, 1) < (\langle N_e' \rangle - \lfloor \langle N_e' \rangle \rfloor) \right]$\;
    $N_e'' \gets \texttt{binomial}(N_e', \text{CCE}(\lambda))$\;
\end{algorithm}
where $\langle N_\gamma \rangle$ is the number of incident photons,
$N_\gamma'$ is the number of absorbed photons,
$\langle N_e \rangle$ is the expected number of electrons,
$N_e'$ is the number of electrons generated,
and $N_e'$ is the number of electrons measured.
For convenience, we've implemented this function as
\href{https://optika.readthedocs.io/en/latest/_autosummary/optika.sensors.electrons_measured.html}{\texttt{optika.sensors.electrons\_measured()}}.
"""
    )
    subsection_noise.append(subsubsection_algorithm)
    subsubsection_charge_spreading = aastex.Subsubsection("Charge Diffusion")
    subsubsection_charge_spreading.append(
        r"""
In most backilluminated imaging sensors used for \UV\ astronomy,
the depletion region (the region with significant electric field) does not 
penetrate all the way into the device.
As a result, there's a so-called field-free region near the back of the sensor
where photoelectrons must undergo a random walk to find their way to the
depletion region where they can then be conducted to the terminals and measured
\citep{Janesick2001}.
This random walk generally leads to a loss of spatial resolution measured by
the sensor since electrons can diffuse to adjacent pixels.
It also leads to an apparent reduction in the noise measured by the sensor since
the blurring due to this diffusion induces a correlation between neighboring 
pixels.

Using Monte Carlo modeling, \citet{Janesick2001} found the following analytic
expression for the standard deviation of the charge diffusion kernel:
\begin{equation}
    \label{eq:chargeDiffusion}
    \sigma_\text{cd}(z) = \begin{cases}
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
we can find the mean variance of the charge diffusion kernel by taking an
average across the entire thickness of the sensor weighted by the probability of
a photon being absorbed at that depth,
\begin{align}
\overline{\sigma}_\text{cd}^2 &= \frac{\int_0^D \sigma_\text{cd}^2(z) e^{-\alpha z} dz}
                                      {\int_0^D e^{-\alpha z} dz} \\
                              &= \frac{z_f \left( \alpha z_f + e^{-\alpha z_f} - 1 \right)}
                                      {\alpha \left( 1 - e^{-\alpha D} \right)}.
\end{align}
The thickness of the depletion region or the field-free region is difficult
to measure, and depends on the voltage applied to the sensor and the charge
collected at the terminals \citep{Stern2004}.

However, \citet{Stern2004} did measure the size of the charge diffusion kernel,
for two discrete wavelengths, of a \goesCcdThickness-thick 
(100 $\Omega$-cm resistivity) \CCD\ for the GOES Soft X-ray Imager.
We can use these measurements to estimate the size of the depletion region
and model the size of the charge diffusion kernel as a function of wavelength.
\cite{Stern2004} didn't directly measure the size of the charge diffusion kernel,
instead they measured a quantity they named the \MCC, the fraction of charge
captured by the central pixel.
Naively, the \MCC\ would be the integral of the charge diffusion kernel over the
extent of a pixel.
However, since a photon can strike anywhere within the central pixel,
we need to convolve with a rectangle function the width of a pixel before
integrating.
So, our definition for the \MCC\ is
\begin{equation}
    P_\text{MCC} = \left\{ \frac{1}{d} \int_{-d/2}^{d/2} \left[ K(x') * \Pi \left( \frac{x'}{d} \right) \right](x) \, dx \right\}^2,
\end{equation}
where $K(x)$ is the charge diffusion kernel,
$\Pi(x)$ is the rectangle function,
and $d$ is the width of a pixel.
If we assume that the charge diffusion kernel is a Gaussian with standard
deviation $\overline{\sigma}_\text{cd}$,
\begin{equation}
    K(x) = \frac{1}{\sqrt{2\pi} \overline{\sigma}_\text{cd}} \exp \left( -\frac{x^2}{2 \overline{\sigma}_\text{cd}^2} \right),
\end{equation}
then we can analytically solve for the \MCC,
\begin{equation}
    \label{eq:mcc}
    P_\text{MCC} = \left\{ \sqrt{\frac{2}{\pi}} \frac{\overline{\sigma}_\text{cd}}{d} \left[ \exp \left( -\frac{d^2}{2 \overline{\sigma}_\text{cd}^2} \right) - 1 \right] + \text{erf} \left( \frac{d}{\sqrt{2} \overline{\sigma}_\text{cd}} \right) \right\}^2,
\end{equation}
where $\text{erf}(x)$ is the error function.

In the top panel of Figure~\ref{fig:chargeDiffusion},
we can have plotted a fit of Equation~\ref{eq:mcc} to the measurements in 
\citet{Stern2004} which found $z_d=\depletionThickness$ best matched the data.
Given the simplicity of our model, 
the fit is surprisingly much better than the models shown in \cite{Stern2004}.
In the lower panel of Figure~\ref{fig:chargeDiffusion},
we've plotted the corresponding standard deviation of the charge diffusion
kernel as a function of wavelength which predicts that the charge diffusion is
reasonably constant over much of the soft X-ray and ultraviolet wavelengths
since the penetration depth is low in this regime.
"""
    )
    subsubsection_charge_spreading.append(ccd_snr.figures.charge_diffusion())
    subsection_noise.append(subsubsection_charge_spreading)
    result.append(subsection_noise)
    return result
