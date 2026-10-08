import numpy as np
import astropy.units as u
import aastex
import ccd_snr

__all__ = [
    "variables",
]


def variables() -> list[aastex.Command]:
    """
    A list of numeric variables used in this article.
    """

    ccd = ccd_snr.ccd()

    return [
        aastex.Variable(
            name="backsurfaceCCE",
            value=np.round(ccd.cce_backsurface, 3),
        ),
        aastex.Variable(
            name="oxideThickness",
            value=np.round(ccd.thickness_oxide),
        ),
        aastex.Variable(
            name="implantThickness",
            value=np.round(ccd.thickness_implant),
        ),
        aastex.Variable(
            name="substrateThickness",
            value=ccd.thickness_substrate,
        ),
        aastex.Variable(
            name="fanoFactor",
            value=np.round(ccd.fano_factor(1 * u.AA).value.ndarray, decimals=3),
        ),
        aastex.Variable(
            name="goesCcdThickness",
            value=ccd.depletion.thickness_substrate,
        ),
        aastex.Variable(
            name="depletionThickness",
            value=np.round(ccd.depletion.thickness, 1),
        ),
        aastex.Variable(
            name="irisMeasuredVmr",
            value=1.5 * u.electron,
        ),
        aastex.Variable(
            name="expectedIrisRatio",
            value=2,
        ),
        aastex.Variable(
            name="expectedWfcRatio",
            value=1.7,
        ),
    ]
