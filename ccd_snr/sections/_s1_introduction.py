import aastex


def introduction() -> aastex.Section:
    result = aastex.Section("Introduction")
    result.append(
        r"""
Back-illuminated, silicon-based image sensors such as \CCDs\ and \CMOS\ sensors 
are ubiquitous in \UV\ astronomy, 
and are currently used in many of the community's most ambitious missions,
such as \AIA\ \citep{Lemen2012}, \IRIS\ \citep{DePontieu2014},
and \WFC\ \citep{Kimble2008} on HST.
Predicting the noise measured by these sensors is important both
for quantifying the uncertainty on current astronomical observations
as well as for evaluating the performance of proposed future instruments.

Often the largest source of noise measured by these sensors is 
shot noise \citep{Stern1986}.
This noise is due to the quantized nature of light \citep{Schottky1918}
and is not a property of the sensor \textit{per se},
but its magnitude depends on the number of interacting photons,
which is determined by the sensor's geometry and optical constants.
Another well-known source of noise inherent to silicon sensors is 
Fano noise \citep{Fano1947},
the random variation of the number of electrons produced
per interacting photon.
This noise source is small \citep{Rodrigues2023},
and often ignored entirely,
but it is usually combined with the shot noise to form a traditional estimate 
of the total noise \citep{Stern1986,Janesick2001}.

This traditional model of shot noise and Fano noise is very accurate in the
visible \citep{Marinelli2024} and X-ray \citep{Ishikawa2011,Athiray2020,Schwab2020}
wavelength regimes.
However, this model appears to be less accurate in the \UV.
For example, \citet{Wulser2018} showed that \IRIS\ measured \textit{less} noise
in the \FUV\ channel than the traditional model would suggest
and similar results were found in the \NUV\ by \WFC\ \citep{Marinelli2024}.
This discrepancy indicates that the traditional model is incomplete, 
and that a more detailed model is needed to predict the noise measured by 
these sensors in the \UV.

In this work, we aim to resolve this discrepancy by developing a noise model
which adds two additional effects to the traditional model.
First, we examine \PCC,
which occurs when electron-hole pairs recombine before they can be measured
by the sensor \citep{Stern1994,Janesick2001}.
Second, we investigate the role of charge diffusion (or charge spreading),
the tendency for photoelectrons to migrate into neighboring pixels \citep{Janesick2001},
a mechanism suggested by both \citet{Wulser2018} and \citet{Marinelli2024} to
resolve this discrepancy.
We will also provide a reference implementation of our model in Python and use
it to predict the noise measured by \AIA, \IRIS, \MUSE, and \WFC.
"""
    )
    return result
