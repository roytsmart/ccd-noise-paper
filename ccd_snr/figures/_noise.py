import matplotlib.pyplot as plt
import aastex
from ._noise_photon import noise_photon
from ._noise_electron import noise_electron

__all__ = [
    "noise",
]


def noise() -> aastex.FigureStar:

    fig, ax = plt.subplots(
        nrows=2,
        figsize=(aastex.text_width_inches, 6),
        constrained_layout=True,
        gridspec_kw=dict(height_ratios=[1, 2]),
        sharex=True,
    )

    noise_photon(ax[0])
    noise_electron(ax[1])

    result = aastex.FigureStar("Noise")
    result.add_fig(fig, width=None)
    result.add_caption(
        aastex.NoEscape(
            r"""
The total and component-wise VSR of our sensor model expressed in two
different units:
photons incident on the sensor (top)
and electrons measured by the sensor (bottom).
Plotted for comparison (gray) is the VSR of the \citet{Stern1986} noise
model.
"""
        )
    )

    return result
