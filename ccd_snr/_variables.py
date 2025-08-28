import numpy as np
import astropy.units as u
import optika
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
            name="bandgapEnergy",
            value=optika.sensors.energy_bandgap,
        ),
        aastex.Variable(
            name="electronHoleEnergy",
            value=optika.sensors.energy_electron_hole,
        ),
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
            name="irisMeasuredVsr",
            value=1.5 * u.electron,
        ),
        aastex.Variable(
            name="irisNaiveVsr",
            value=2 * u.electron,
        ),
        aastex.Variable(
            name="irisModeledVsr",
            value=np.round(
                a=ccd_snr.instruments.iris.fano_electron[
                    ccd_snr.instruments.iris.index_1330
                ].ndarray,
                decimals=2,
            ),
        ),
        aastex.Variable(
            name="irisWavelength",
            value=ccd_snr.instruments.iris.wavelength[
                ccd_snr.instruments.iris.index_1330
            ].ndarray,
        ),
        aastex.Variable(
            name="diffusionWavelength",
            value=ccd_snr.diffusion.wavelength,
        ),
        aastex.Variable(
            name="diffusionPixelSize",
            value=ccd_snr.diffusion.width_pixel,
        ),
    ]
