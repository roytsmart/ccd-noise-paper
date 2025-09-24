import aastex


def introduction() -> aastex.Section:
    result = aastex.Section("Introduction")
    result.append(
        r"""
Backilluminated, silicon-based image sensors such as \CCDs\ and \CMOS\ sensors 
are ubiquitous in \UV\ astronomy, 
and are currently used in many of the community's most ambitious missions,
such as \AIA\ \citep{Lemen2012}, \IRIS\ \citep{DePontieu2014},
and \WFC\ \citep{Kimble2008} on the HST.
Predicting the noise introduced by these sensors is important for determining the
performance of future astronomical instruments and to examine if a given
measurement is feasible.
Understanding this noise is also useful for characterizing current astronomical
observations since it allows for better quantification of uncertainties for
wavelengths where a detailed noise measurement is not available.

Often the largest source of noise on images captured by these sensors is 
shot noise \citep{Stern1986}.
This noise is due to the quantized nature of light \citep{Schottky1918}
and is not a property of the sensor \textit{per se},
but the fraction of incident light that interacts with the sensor determines 
the magnitude of the shot noise.
Another well-known source of noise inherent to silicon-based sensors is 
Fano noise \citep{Fano1947},
the unavoidable variation of the number of electrons produced
per interacting photon.
This noise source is small \citep{Rodrigues2023},
and often ignored entirely,
but it is usually combined with the shot noise to estimate the total noise
measured by these sensors \citep{Stern1986,Janesick2001}.

This traditional model works well in the X-ray regime \cite{Athiray2020}
and is often ignored entirely,
but is needed to 
The Fano noise is usually considered to be the only noise contribution from the
charge-generation process within the silicon \citep{Janesick2001}, and is
often added to the photon shot noise \citep{Schottky1918} to estimate the
total error measured by the sensor.

This traditional model of shot noise and Fano noise is sufficient in X-ray 
wavelengths \cite{Athiray2020},
and in visible light wavelengths where there is no Fano noise.
However, in \citet{Wulser2018} they showed that \IRIS\ measured \textit{less} noise
in the \FUV\ than the traditional model would suggest and
similar results were found in the \NUV\ by \WFC\ \citep{Marinelli2024}.
These results show that the traditional model is incomplete and that a more
complicated model is needed to fully explain the observed noise statistics.

In this work, we will propose a model where the phenomenon of \PCC\ accounts
for this observed discrepancy.
"""
    )
    return result
