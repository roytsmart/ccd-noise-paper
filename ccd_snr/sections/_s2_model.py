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
    \text{QE}(\lambda) = \frac{N_{e}}{N_\gamma}
                       = A(\lambda) \times \text{IQY}(\lambda) \times \text{CCE}(\lambda),
\end{equation}
where $N_e$ is the number of electrons measured by the sensor for a 
given wavelength $\lambda$,
$N_\gamma$ is the total number of photons incident on the sensor,
$A(\lambda)$ is the fraction of incident energy absorbed by the epitaxial layer, 
$\text{IQY}(\lambda)$ is the ideal \QY,
the average number of photoelectrons generated per absorbed photon,
and $\text{CCE}(\lambda)$ is the charge-collection efficiency,
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
and $E_\text{eh} = \electronHoleEnergy$ is the mean energy required to generate
one electron-hole pair at room temperature.
Surprisingly, despite initial results to the contrary \citep{Fraser1994},
this simple relation is a good approximation across the entire wavelength range
considered \citep{Geist1996,Scholze1998,Fang2019}.

In \citet{Stern1994}, the CCE is expressed in terms of a differential CCE,
$\eta(z)$, which is the fraction of photoelectrons collected for a photon 
absorbed at a depth $z$ into the epitaxial layer.
The total CCE is then the average differential CCE weighted by 
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
of the differential CCE,
\begin{equation} \label{differential-cce}
    \eta(z) = \begin{cases}
        \eta_0 + (1 - \eta_0) z / W, & 0 < z < W \\
        1, & W < z < \infty
    \end{cases}
\end{equation}
where $\eta_0$ is the differential CCE at the back surface of the sensor.
Plugging Equation \ref{differential-cce} into Equation \ref{cce} yields an
arithmetic expression for the CCE,
\begin{equation}
    \text{CCE}(\lambda) = \eta_0 + \left( \frac{1 - \eta_0}{\alpha W} \right)(1 - e^{-\alpha W}),
\end{equation}
which can be used in Equation \ref{eq:quantum-efficiency} to determine the \QE.
In Figure \ref{fig:absorbanceAndCCE} we have plotted $\text{CCE}(\lambda)$ for
the \citet{Heymes2020} parameters in Table \ref{table:models}.

In \citet{Stern1994}, the authors define an effective \QE\ as
\begin{equation} \label{eqe}
    \text{EQE}(\lambda) = A(\lambda) \times \text{CCE}(\lambda),
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
    subsection_noise.append(
        r"""
Our noise model will consider three sources:
shot noise from the random arrival time of the photons striking the sensor,
Fano noise due to inherent randomness in the process which converts photons
to electrons,
and noise due to electrons randomly recombining before they can be measured by
the sensor.
This section will describe the statistics of each noise source and demonstrate
a fast algorithm which can simulate the noise measured by our model sensor
for a given number of incident photons.

Throughout this work, we will measure noise in terms of a \VSR
\footnote{statisticians might call the \VSR\ the Fano factor, but to avoid
confusion with the Fano \textit{noise} we have chosen to use a different term
to describe this quantity.},
\begin{equation}
    \text{VSR}(X) = \frac{\text{Var}(X)}{\langle X \rangle},
\end{equation}
where $X$ is some random variable,
$\text{Var}(X)$ is the variance of $X$,
and $\langle X \rangle$ denotes the expectation value of $X$.
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
noise \citep{Fano1947}, the unpredictable variation of \QY, 
the number of electrons generated per absorbed photon.
Fano noise is usually expressed in terms of the Fano factor, 
$\mathcal{F} = \text{VSR}(q)$,
where $q$ is a random variable representing a sample from the distribution
of \QY.
Silicon is commonly accepted to have $\mathcal{F} \approx 0.1$ \citep{Janesick2001}.
In part due to variations of the Fano noise as a function of wavelength and
temperature \citep{Fraser1994}, 
there is some disagreement in the literature around a more precise value for
$\mathcal{F}$ 
\citep[\& references therein]{Fraser1994,Lowe1997,Mazziotta2008,Kotov2018,Rodrigues2021,Rodrigues2023}.

$\mathcal{F}$ is routinely measured in the \SXR\ region
(typically with \SI{6}{\kilo\electronvolt} photons emitted from $^{55}$Fe sources),
where the Fano noise is much larger than the typical readout noise
and $\text{CCE}(\lambda)$ is nearly unity.
However, $\mathcal{F}$ must be larger than the accepted value in the \UV\
(where $\text{IQY}(\lambda)$ is near unity)
since it is impossible to construct any distribution narrow enough to be 
consistent with both Equation~\ref{eq:iqy}
(which is well-supported in the literature)
and $\mathcal{F} \approx 0.1$ due to the discrete nature of electrons.
Unfortunately, resolving this inconsistency by measuring
$\mathcal{F}$ in this regime is difficult since the 
Fano noise is comparable to the readout noise,
and we were not able to find any \UV\ measurements of $\mathcal{F}$
in the literature.
So, we adopt a simple, ad-hoc model of the Fano noise with the correct limiting
behavior, 
described in the following paragraphs.
Because the Fano noise is so small compared to the other noise sources
considered in this study, the precise form of this noise model does not
appreciably influence our conclusions.

At high energies, Fano noise is well-described by a Gaussian distribution
\citep{Rodrigues2023},
but at low energies, a Gaussian distribution is problematic since it becomes likely
that it will be negative for some samples (which is unphysical).
So, we desire an underdispersed (\VSR\ < 1), discrete distribution supported on 
the natural numbers which tends towards a Gaussian as its expectation value 
approaches infinity.
Perhaps the most well-studied distribution which has these properties is the
Conway-Maxwell-Poisson distribution \citep{Huang2020},
but the parameters of this distribution can be difficult to interpret 
and it does not have an implementation in the standard scientific Python ecosystem.
Instead, we will use the following compound distribution,
parameterized by the mean $\mu$ and the asymptotic \VSR\ $\nu$,
\begin{equation} \label{eq:discrete-gamma}
    \text{SR}\Gamma(\mu, \nu) = \text{SR}(\Gamma(\mu / \nu, \nu)),
\end{equation}
where $\Gamma(k, \theta)$ is the gamma distribution with shape parameter
$k$ and scale parameter $\theta$, and
\begin{equation} \label{eq:stochastic-rounding}
    \text{SR}(x) = \begin{cases}
        \lfloor x \rfloor, \quad \text{with probability $\lceil x \rceil - x$} \\
        \lceil x \rceil, \quad \text{with probability $x - \lfloor x \rfloor$},
    \end{cases}
\end{equation}
is a stochastic rounding function \citep{Croci2022} which randomly discretizes
a continuous random variable $x$ onto the integers without changing the mean of $x$.
We chose to use Equation~\ref{eq:stochastic-rounding} instead of a deterministic
rounding scheme so that our distribution will satisfy Equation~\ref{eq:iqy},
which as we explained in Section~\ref{subsec:Signal},
is an unreasonably good approximation of $\text{IQY}(\lambda)$ over the entire 
wavelength range considered in this study.

Therefore, if we approximate the quantum yield of the $i$th photon absorbed by the
sensor as
\begin{equation}
    q_i' \leftarrow \text{SR}\Gamma(\text{IQY}(\lambda), \mathcal{F}),
\end{equation}
where $\mathcal{F} = \fanoFactor$ is the best available measurement of $\mathcal{F}$ at 
\SI{6}{\kilo\electronvolt} \citep{Rodrigues2021},
then the total number of electrons generated given $N_\gamma'$ absorbed photons is simply
\begin{equation} \label{eq:totalElectrons}
    N_e' = \sum_{i=0}^{N_\gamma'} q_i'.
\end{equation}
However, a sum is inconvenient here since it increases the computation time as the
incident flux increases.
Therefore, we will approximate Equation~\ref{eq:totalElectrons} using a 
variance-matching procedure as
\begin{equation} \label{eq:approxTotalElectrons}
    N_e' \simeq \text{SR}\Gamma(N_\gamma' \; \text{IQY}(\lambda), \mathcal{F}'),
\end{equation}
where the effective Fano factor which accounts for discretization effects is
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
    subsubsection_noise_fano.append(ccd_snr.figures.noise_fano())
    subsubsection_noise_fano.append(
        r"""
In Figure~\ref{fig:fanoNoise}, we have plotted the \VSR\ as a function of wavelength
of a Monte Carlo sampling of
Equations~\ref{eq:totalElectrons}~and~\ref{eq:approxTotalElectrons}
to demonstrate the validity of our approximation.
Note the tight agreement between the expressions in the \SXR/\UV\ 
and the slight deviation in the visible, where $\text{IQY}(\lambda) = 1$.
Figure~\ref{fig:fanoNoise} also demonstrates that it is impossible to create
a discrete distribution consistent with the Fano factor in regions where
$\text{IQY}(\lambda)$ is small. 
The width of our distribution increases as 
$\text{IQY}(\lambda)$ decreases and plateaus since $\text{IQY}(\lambda)$ can not
go below unity for the wavelength range considered in this study. 

In Figure~\ref{fig:Noise} we can see the 
contribution of Fano noise to the total noise measured by our simulated sensor.
Note how the Fano noise component is very small compared to the photon shot noise.
"""
    )
    subsection_noise.append(subsubsection_noise_fano)
    subsubsection_noise_recombination = aastex.Subsubsection("Recombination Noise")
    subsubsection_noise_recombination.append(ccd_snr.figures.energy_spectrum())
    subsubsection_noise_recombination.append(
        r"""
Recombination of photoelectrons in the \PCC\ region is a significant source of noise in
the \UV\ since the photons are absorbed so close to the surface,
where the CCE is relatively low (Figure \ref{fig:absorbanceAndCCE}).
In the \citet{Stern1994} model, 
each photoelectron generated in the \PCC\ region has a probability 
$\eta(x)$ of \textit{not} recombining and subsequently being measured 
by the sensor.
We can express this using a binomial distribution, 
\begin{equation}
    q_i'' \leftarrow \text{B}(q_i', \eta(z_i)),
\end{equation}
where $q_i''$ is the measured quantum yield of the $i$th photon,
$z_i$ is the penetration depth of the $i$th photon.
and $\text{B}(n, p)$ is a sample from the binomial distribution
with $n$ trials and probability of success $p$.
The total number of measured electrons given $N_\gamma'$ absorbed photons is then
\begin{equation} \label{eq:measuredElectrons}
    N_e'' = \sum_{i=0}^{N_\gamma'} q_i''.
\end{equation}
We can remove the sum in Equation~\ref{eq:measuredElectrons} in a similar 
way to Equation~\ref{eq:approxTotalElectrons} by treating the \PCC\ region and 
its complement, the \CCC\ region, separately so that
\begin{equation} \label{eq:approxMeasuredElectrons}
    N_e'' = n_e'' + m_e'',
\end{equation}
where $n_e''$ is the number of electrons measured from the \CCC\ region
and $m_e''$ is the number of electrons measured from the \PCC\ region.
We can easily compute the signal generated in the \CCC\ region using
Equation~\ref{eq:approxTotalElectrons},
\begin{equation}
    n_e'' = \text{SR}\Gamma(n_\gamma' \, \text{IQY}(\lambda), \mathcal{F}'),
\end{equation}
where the number of photons absorbed in the \CCC\ region, $n_\gamma'$, 
is found by drawing from a binomial distribution,
\begin{equation}
    n_\gamma' \leftarrow \text{B}(N_\gamma', p_c),
\end{equation}
with a probability $p_c = e^{-\alpha W}$ of a photon being absorbed in
the \CCC\ region.

In the \PCC\ region,
the distribution of measured electrons is a sum of binomial distributions,
where each term of the sum has a different number of trials and probability
of success,
\begin{equation} \label{eq:partialElectrons}
    m_e'' = \sum_{i=0}^{m_\gamma'} \text{B}(q_i', \eta(z_i)),
\end{equation}
where $m_\gamma' = N_\gamma' - n_\gamma'$ is the number of photons absorbed in
the \PCC\ region.
Using Equation~\ref{differential-cce},
we can apply a change of variables to the exponentially-distributed
penetration depth, $z_i$, to find the \PDF\ of $\eta(z_i)$ as
\begin{equation}
    p_\eta = \frac{\alpha W e^{\frac{\alpha W (1 - \eta)}{1 - \eta_0}}}{(1 - \eta_0)(e^{\alpha W} - 1)} .
\end{equation}
Given this distribution of $\eta(z_i)$, 
it is not possible to solve the sum in Equation~\ref{eq:partialElectrons} analytically,
but we can compute the mean and variance the sum using the expressions
given by \citet{heropup2019}:
\begin{align}
    \text{EBS}(\mu_n, \mu_p) &= \biggl \langle \frac{1}{N} \sum_{i=0}^N \text{B}(n_i, p_i) \biggr \rangle \\
                            &= \mu_n \mu_p
\end{align}
and
\begin{align} 
    &\text{VBS}(\mu_n, \mu_p, \sigma_n^2, \sigma_p^2) = \text{Var}\left(\frac{1}{N} \sum_{i=0}^N \text{B}(n_i, p_i) \right) \\
                            &= \sigma_n^2 \sigma_p^2 + \sigma_n^2 \mu_p^2 + \mu_n^2 \sigma_p^2 + \mu_n (\mu_p - \sigma_p^2 - \mu_p^2),
\end{align}
where $\mu_n$, $\mu_p$, $\sigma_n^2$, and $\sigma_p^2$ are the mean and variance
of the number of trials, $n$, and probability of success $p$.
The mean and variance of $m_e''$ is then
\begin{equation} \label{eq:signalMean}
    \langle m_e'' \rangle = m_\gamma' \, \text{EBS}(\mu_q, \mu_\eta)
\end{equation}
and
\begin{equation} \label{eq:signalVar}
    \text{Var}(m_e'') = m_\gamma' \, \text{VBS}(\mu_q, \mu_\eta, \sigma_q^2, \sigma_\eta^2),
\end{equation}
where
\begin{equation}
    \mu_q = \text{IQY}(\lambda).
\end{equation}
and
\begin{equation}
    \sigma_q^2 = \mathcal{F}' \mu_q,
\end{equation}
is the mean and variance of the quantum yield $q_i'$, and
\begin{equation}
    \mu_\eta = \eta_0 + \frac{1 - \eta_0}{\alpha W} + \frac{1 - \eta_0}{1 - e^{\alpha W}},
\end{equation}
and
\begin{equation}
    \sigma_\eta^2 = \frac{1}{4} (1 - \eta_0)^2 \left[ \frac{4}{\alpha^2 W^2} - \text{csch}^2 \left( \frac{\alpha W}{2} \right) \right]
\end{equation}
is the mean and variance of $\eta(z_i)$ within the \PCC\ region.
Using Equations~\ref{eq:signalMean} and~\ref{eq:signalVar},
we can crudely approximate Equation~\ref{eq:partialElectrons} using another
$\text{SR}\Gamma(\mu, \nu)$ distribution,
\begin{equation} \label{eq:approxPartialElectrons}
    m_e'' \simeq \text{SR}\Gamma(\langle m_e'' \rangle, \text{VSR}(m_e'') - 1/6 \langle m_e'' \rangle),
\end{equation}
which has the same mean and variance as Equation~\ref{eq:partialElectrons}.

Equation~\ref{eq:approxMeasuredElectrons} allows us to sample the distribution
of measured electrons efficiently enough to be useful in an instrument forward
model.
We've provided a reference implementation of Equation~\ref{eq:approxMeasuredElectrons}
in Python,
\href{https://optika.readthedocs.io/en/latest/_autosummary/optika.sensors.signal.html}{\texttt{optika.sensors.signal()}},
to ease adoption of this method into existing instrument pipelines.

In Figure~\ref{fig:energySpectrum},
we have plotted the probability of measuring a given number of electrons
using Monte Carlo simulations of Equation~\ref{eq:measuredElectrons} 
and Equation~\ref{eq:approxMeasuredElectrons}
to demonstrate the quality of our approximation.
In the \FUV\ and \EUV\ we can see that this approximation is extremely accurate,
only in the \SXR\ does this approximation deviate slightly from the true
distribution.

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
    subsection_charge_spreading.append(ccd_snr.figures.charge_diffusion())
    subsection_charge_spreading.append(ccd_snr.figures.diffusion_kernel())
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
and $\text{erf}(x)$ is the error function.

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
We used the \IRIS\ pixel size of \diffusionPixelSize\ and a wavelength of
\diffusionWavelength\ to demonstrate the worst-case scenario for \IRIS.
This kernel is intended to be convolved with an input image after the noise
model (described above) has been applied to approximate the effects of charge
diffusion and complete the forward model of the sensor.
"""
    )
    result.append(subsection_charge_spreading)

    return result
