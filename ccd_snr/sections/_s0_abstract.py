import aastex

__all__ = [
    "abstract",
]


def abstract() -> aastex.Abstract:
    result = aastex.Abstract()
    result.append(
        r"""
Silicon-based imaging sensors are a critical component for \UV\ astronomy.
Their high sensitivity and low noise are a vital part of making
\UV\ telescopes practical to build.
However, \UV\ light is unique compared to other components of the
electromagnetic spectrum since it has a shallow penetration depth
into the silicon substrate and is absorbed in a region where the corresponding 
electron-hole pairs have a significant chance of recombination before being measured.
This phenomenon is known as \PCC, 
and in this article we will use the theoretical 
sensor described in \citet{Stern1994}
as the basis for a noise model which accounts for \PCC\ and is
valid from the soft X-ray to the near-infrared (0.1-1000 nm).
Using this model, we will show that considering the effect of \PCC\
improves the predicted \SNR\ of a silicon sensor in the \UV\ by up to $\sqrt{2}$
compared to a model which does not consider recombination.
We will evaluate this model for the \AIA, \IRIS, \MUSE, and \WFC\ instruments and find that
our model predicts a significant improvement in the expected \SNR\ of some 
channels of each instrument.
We will also develop a procedure which can efficiently sample the distribution
of measured electrons and is suitable for use in forward models of astronomical
instruments.
\acresetall
"""
    )
    return result
