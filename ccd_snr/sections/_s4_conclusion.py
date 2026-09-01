import aastex

__all__ = [
    "conclusion",
]


def conclusion() -> aastex.Section:
    result = aastex.Section("Conclusions and Future Work")
    result.packages.append(
        aastex.Package(name="algorithm2e", options="ruled"),
    )
    result.append(r"""
This work aims to resolve the discrepancy identified by 
\citet{Borders2010} and \citet{Wulser2018} in the predicted vs. observed noise
measured by back-illuminated silicon imaging sensors.
To accomplish this, we reconsidered the effects of \PCC\ and charge diffusion
on the noise by developing a simple model of a back-illuminated sensor
based on the \CCE\ introduced by \citet{Stern1994} and a charge diffusion model
found by \citet{Janesick2001}.
By analyzing these effects in a self-consistent manner, we were able to mostly
resolve the discrepancy, and we propose that \PCC\ is the most important
effect to consider in the \UV.
The width of the charge diffusion kernel is nearly independent of wavelength,
but its effect on the \VMR\ is not, since diffusion suppresses the
photon-correlated term, which grows with the quantum yield.

Our sensor model predicts that there are two \UV\ bands, 
\qtyrange[range-units=single,range-phrase=-]{30}{100}{\angstrom} 
and \qtyrange[range-units=single,range-phrase=-]{500}{2000}{\angstrom},
where \PCC\ effects should be considered for a correct noise estimate.
We evaluated our sensor model for some popular and upcoming \UV\
astronomical instruments and found that there are a few channels in each 
instrument where our model implies that the \SNR\ is better than the traditional
model would suggest.
We also have provided a reference implementation of our sensor model in Python,
\href{https://optika.readthedocs.io/en/latest/_autosummary/optika.sensors.html}{\texttt{optika.sensors}},
to make this noise model simple to integrate with existing instrument data
processing pipelines.

This work does not consider read noise or other noise sources since those
will be specific to the particular camera electronics of each instrument,
and also cannot be characterized using a \VMR.
Instead, this work focuses only on the noise intrinsic to the charge-generation
process, since this is comparatively consistent across different instruments.

We plan to use this work to model the noise for \ESIS\ \citep{Parker2022},
as well as \FURST, sounding-rocket-based spectrographs developed by our
research group for observing the solar atmosphere.
""")
    return result
