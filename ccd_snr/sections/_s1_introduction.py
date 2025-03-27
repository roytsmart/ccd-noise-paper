import aastex


def introduction() -> aastex.Section:
    result = aastex.Section("Introduction")
    result.append(
        r"""
Backilluminated, silicon-based image sensors such as \CCDs\ and \CMOS\ sensors 
are ubiquitous in \UV\ astronomy, 
and are currently used in many of the community's most ambitious missions,
such as \AIA\ \citep{Lemen2012}, \IRIS\ \citep{DePontieu2014},
and \WFC\ \citep{Kimble2008}.
Despite their popularity,
understanding the noise statistics of these sensors in the \UV\
is challenging due to the phenomenon of \PCC,
where electron-hole pairs generated near the back surface of the sensor
(due to the shallow penetration depth of \UV\ photons)
recombine before they can be measured \citep{Janesick2001}.
\PCC\ can be difficult to quantify since it depends on how the back surface
of the sensor was prepared by the manufacturer,
and directly measuring it is complicated by other effects such as transmission
through the illuminated surface and charge diffusion \citep{Janesick2001}.
The effect of \PCC\ has been considered for modeling instruments searching for 
dark matter \citep{Rodrigues2023},
but it has not been incorporated into the noise model of any astronomical
\UV\ instrument that we are aware of, including \AIA\ \citep{Boerner2012}, 
\IRIS\ \citep{Wulser2018}, and \WFC\ \citep{Marinelli2024}.
In this work, we will model \PCC\ using the simple, ad-hoc method described in
\citet{Stern1994} and investigate its effects on the noise measured by a typical
sensor.

Another poorly-understood source of noise in silicon imaging sensors is
Fano noise \citep{Fano1947}, 
the unavoidable variation in the quantum yield, the number of electrons measured per photon.
Fano noise is routinely measured in the soft X-ray regime \citep{Rodrigues2023},
but is rarely measured in the \UV\ despite being predicted to
have significant width and skew
variations as a function of wavelength \citep{Fraser1994}.
Since the Fano noise in silicon is so small,
this work will use a very simple model of constant Fano noise,
which has been designed to generate non-negative quantum yields in regimes where
the quantum yield is low, such as the \UV.

We will use these two noise sources along with photon shot noise
to develop a computationally-efficient noise model which can
predict the total noise we expect to measure using a silicon sensor.
This work will not consider read noise since it is a quantity that depends on the
camera electronics.
This model will be used to demonstrate the importance of modeling recombination by
comparing it to the \citet{Stern1986} noise model which considers only shot noise
and Fano noise.
We will then evaluate this model for several popular \UV\ instruments
and predict the amount of noise for the nominal wavelengths of each instrument.
Finally, we will possibly resolve the discrepancies described in \citep{Wulser2018}
and \citep{Marinelli2024} regarding the shallower-than-expected slopes of the 
photon-transfer curves of \IRIS\ and \WFC.
"""
    )
    return result
