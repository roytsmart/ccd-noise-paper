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
    ] + _tracks()


def _tracks() -> list[aastex.Command]:
    """The variables describing the particle-track measurement of the appendix."""
    chips = ["FUV1", "FUV2", "SJI"]
    sji = ccd_snr.tracks.summary("SJI")
    num_frames = sum(ccd_snr.tables.num_frames(c)[0] for c in ["FUV1", "SJI"])
    return [
        aastex.Variable("numTrackFrames", num_frames),
        aastex.Variable(
            "numTracks",
            sum(ccd_snr.tracks.summary(c).num_tracks for c in chips),
        ),
        aastex.Variable(
            "numFlatTracks",
            sum(ccd_snr.tracks.summary(c).num_flat for c in chips),
        ),
        aastex.Variable("numFlatTracksSji", sji.num_flat),
        aastex.Variable("sjiSamePixel", f"{sji.same_pixel:.2f}"),
        aastex.Variable("sjiSamePixelError", f"{sji.same_pixel_error:.2f}"),
        aastex.Variable("sjiSamePixelModel", f"{sji.same_pixel_paper:.2f}"),
        aastex.Variable("sjiCriticalDepth", f"{sji.critical_depth[1]:.2f}"),
        aastex.Variable("sjiWidthMax", f"{sji.width_max[1].to_value(u.um):.1f}"),
        aastex.Variable(
            "modelCriticalDepth",
            f"{ccd_snr.tracks.paper_model()[0]:.2f}",
        ),
    ]
