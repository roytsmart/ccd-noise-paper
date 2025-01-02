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
of width $W$, where some of the generated photoelectrons recombine before being
measured by the sensor.
\PCC\ is usually described by quantity called \CCE, the fraction of 
photoelectrons which do \textit{not} recombine and are measured by the sensor.
In Section \ref{subsec:Noise} we will see how \PCC\
affects the variance of the signal measured by an imaging sensor.
"""
    )
    subsection_qe = aastex.Subsection("Quantum Efficiency")
    subsection_qe.append(ccd_snr.figures.absorbance_and_cce())
    subsection_qe.append(ccd_snr.figures.qe_effective())
    subsection_qe.append(ccd_snr.tables.models())
    subsection_qe.append(
        r"""
\QE\ is the average number of photoelectrons measured per photon and is a common 
performance metric for measuring sensor sensitivity.
It is given in \citet{Janesick2001} as
\begin{equation} \label{eq:quantum-efficiency}
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
\begin{equation} \label{eq:iqy}
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
which can be used in Equation \ref{eq:quantum-efficiency} to determine the \QE.
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
    result.append(subsection_qe)

    subsection_noise = aastex.Subsection("Noise")
    subsection_noise.append(ccd_snr.figures.noise_photon())
    subsection_noise.append(ccd_snr.figures.noise_electron())
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

Throughout this work, we will measure noise in terms of a \VSR
\footnote{statisticians might call the \VSR\ the Fano factor, but to avoid
confusion with the Fano \textit{noise} we've chosen to use a different term
to describe this quantity.},
\begin{equation}
    \text{VSR}(X) = \frac{\text{Var}(X)}{\langle X \rangle},
\end{equation}
where $X$ is a random variable,
$\text{Var}(X)$ is the variance of $X$,
and $\langle X \rangle$ denotes the expectation value of $X$.
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
Shot noise from the random arrival time of each photon is often the leading 
noise contributor in \UV\ solar astronomy \citep{Lemen2012, DePontieu2014}.
It is described by a Poisson distribution,
\begin{equation} \label{eq:shot-noise-variance}
    N_\gamma' = \text{Pois}(A(\lambda) \langle N_\gamma \rangle),
\end{equation}
where $\langle N_\gamma \rangle$ is the expected number of incident photons,
$N_\gamma'$ is the number of photons which interact with the light-sensitive
region of the sensor,
and $\text{Pois}(x)$ is a sample from the Poisson distribution.

In Figures~\ref{fig:photonNoise}~and~\ref{fig:electronNoise}
we've plotted the \VSR\ of the shot noise in blue.
In Figure~\ref{fig:photonNoise}, we can see that the \VSR\ of the shot noise
relative to the number of incident photons is often unity since it's
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
noise \citep{Fano1947}, the unpredictable variation of the number of electrons.
generated per photon.
Fano noise is usually expressed in terms of the Fano factor, 
$\mathcal{F} = \sigma^2 / \mu$,
the ratio of the variance to the mean of some random process 
(very similar to our definition of \VSR\ above).

The Fano noise for silicon is commonly accepted to have
$\mathcal{F} \approx 0.1$ \citep{Janesick2001}.
In part due to variations of the Fano noise as a function of wavelength and
temperature \citep{Fraser1994}, 
there is some disagreement in the literature around a more precise value for
$\mathcal{F}$ 
\citep[\& references therein]{Fraser1994,Lowe1997,Mazziotta2008,Kotov2018,Rodrigues2021,Rodrigues2023}.
$\mathcal{F}$ is often measured in the \SXR\ region,
traditionally with $^{55}$Fe sources, which have a high $\text{IQY}(\lambda)$.
For \UV\ wavelengths, where the $\text{IQY}(\lambda)$ is near unity,
it becomes impossible to construct a distribution narrow enough to be consistent 
with a Fano factor that small (Figure~\ref{fig:fanoNoise}).
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
    q_i \leftarrow \mathcal{F} \; \text{Pois}\left( \frac{\text{IQY}(\lambda)}{\mathcal{F}} \right),
\end{equation}
where $q_i$ is the fano-noise-perturbed quantum yield of the $i$th photon.
Equation \ref{eq:scaled-poisson} has the nice property of reproducing a Gaussian 
with the correct width at high energies while also being non-negative around
$\text{IQY}(\lambda) \approx 1$.
Obviously, Equation \ref{eq:scaled-poisson} does not yield an integer number of electrons,
so it can't be a sample of the distribution, it still represents an intermediate 
expectation value.
In Section~\ref{subsec:QuantumEfficiency},
we explained that Equation~\ref{eq:iqy} was an unreasonably good approximation
over the entire wavelength range considered in this study.
To satisfy Equation~\ref{eq:iqy},
we must discretize Equation~\ref{eq:scaled-poisson} in such a way that the
expectation value is unchanged.
A simple distribution which has these properties is
\begin{equation}
    \label{eq:discretization}
    q_i' \leftarrow \lfloor q_i \rfloor + \text{B}(1, \{ q_i \})
\end{equation}
where $q_i'$ is the total quantum yield of the $i$th photon,
$\lfloor x \rfloor$ denotes the floor function,
$\{ x \}$ is the fractional part of $x$, 
and $\text{B}(n, p)$ is a sample from the binomial distribution
for $n$ trials with probability $p$.
Equation \ref{eq:discretization} is a choice between the two closest integers 
to $q_i$ with the probabilities weighted to conserve the mean of the distribution.
One consequence of this distribution is that it increases the apparent Fano noise
if $\text{IQY}(\lambda)$ is near unity due to discretization effects.
This apparent increase in Fano noise is not unprecedented and may
explain the sawtooth variations in the Fano noise observed by \citet{Santos1991}.

To compute the total number of electrons generated given the number of photons absorbed, 
we need to sum $q_i'$ over $N_\gamma'$ photons,
\begin{equation} \label{eq:totalElectrons}
    N_e' \leftarrow \sum_{i=0}^{N_\gamma'} \bigl[ \lfloor q_i \rfloor + \text{B}_i(1, \{ q_i \}) \bigr].
\end{equation}
However, a sum is inconvenient here since it increases the computation time as the
incident flux increases.
Since $\sum_i \text{Pois}(x_i) = \text{Pois}(\sum_i x_i)$ \citep{Lehmann1986}, 
we can approximate Equation~\ref{eq:totalElectrons} using a variance-matching
procedure as
\begin{equation} \label{eq:approxTotalElectrons}
    N_e' \simeq \lfloor N_e \rfloor + \text{B}_i(1, \{ N_e \}),
\end{equation}
where
\begin{equation}
    N_e \leftarrow \mathcal{F}' \; \text{Pois} \left(\frac{N_\gamma' \; \text{IQY}(\lambda)}{\mathcal{F}'} \right),
\end{equation}
and the effective Fano factor which accounts for discretization effects is
\begin{equation}
    \mathcal{F}' = \mathcal{F} + \frac{1}{6} \frac{N_\gamma' - 1}{N_\gamma' \; \text{IQY}(\lambda)}
\end{equation}
since each term in Equation~\ref{eq:totalElectrons} increases the variance
of $N_e'$ by approximately twice the variance of the rectangle function.
Equation~\ref{eq:approxTotalElectrons} approximates Equation~\ref{eq:totalElectrons}
extremely well,
only when $\text{IQY}(\lambda)$ is in the range 1.0 to 1.25 does this approximation
deviate by a few percent from the exact expression.
"""
    )
    # subsubsection_noise_fano.append(ccd_snr.figures.noise_fano())
    subsubsection_noise_fano.append(
        r"""
In Figure~\ref{fig:fanoNoise}, we've plotted the \VSR\ as a function of wavelength
of a Monte Carlo sampling of
Equations~\ref{eq:totalElectrons}~and~\ref{eq:approxTotalElectrons}
to demonstrate the validity of our approximation.
Note the tight agreement between the expressions in the \SXR/\UV\ 
and the slight deviation in the visible, where $\text{IQY}(\lambda) = 1$.
Figure~\ref{fig:fanoNoise} also demonstrates that it is impossible to create
a discrete distribution consistent with the Fano factor in regions where
$\text{IQY}(\lambda)$ is small. 
The width of our distribution increases as 
$\text{IQY}(\lambda)$ decreases and plateaus since $\text{IQY}(\lambda)$ can't
go below unity for the wavelength range considered in this study. 

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
In the \citet{Stern1994} model, 
each photoelectron generated in the \PCC\ region has a probability 
$\text{CCE}(\lambda)$ of \textit{not} recombining and subsequently being measured 
by the sensor.
We can express this using a binomial distribution,
\begin{equation} \label{eq:recombination}
    N_e'' \leftarrow \text{B}(N_e', \text{CCE}(\lambda)),
\end{equation}
where $N_e''$ is the actual number of electrons measured by the sensor.

In Figures \ref{fig:photonNoise} and \ref{fig:electronNoise} we can see that the
recombination noise is the dominant source of noise measured by the sensor
in the near/far \UV\ and remains non-negligible into the \EUV.
"""
    )
    subsection_noise.append(subsubsection_noise_recombination)
    subsubsection_algorithm = aastex.Subsubsection("Sampling Algorithm")
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
    $N_e \gets \texttt{poisson}(\langle N_e \rangle / \mathcal{F}') \times \mathcal{F}'$\;
    $N_e' \gets \lfloor  N_e \rfloor + \texttt{binomial}(1, \{ N_e \})$\;
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
    # subsection_noise.append(subsubsection_algorithm)
    result.append(subsection_noise)

    subsection_charge_spreading = aastex.Subsection("Charge Diffusion")
    subsection_charge_spreading.append(ccd_snr.figures.charge_diffusion())
    subsection_charge_spreading.append(ccd_snr.figures.diffusion_kernel())
    subsection_charge_spreading.append(
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
and $\text{erf}(x)$ is the error function.

In the top panel of Figure~\ref{fig:chargeDiffusion},
we've  plotted a fit of Equation~\ref{eq:mcc} to the measurements in 
\citet{Stern2004} which found $z_d=\depletionThickness$ best matched the data.
Given the simplicity of our model, 
the fit is surprisingly much better than the models shown in \cite{Stern2004}.
In the lower panel of Figure~\ref{fig:chargeDiffusion},
we've plotted the corresponding standard deviation of the charge diffusion
kernel as a function of wavelength which predicts that the charge diffusion is
reasonably constant over much of the \SXR\ and ultraviolet wavelengths
since the penetration depth is low in this regime.
"""
    )
    result.append(subsection_charge_spreading)

    return result
