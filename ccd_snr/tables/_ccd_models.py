import pylatex
import astropy.units as u
import ccd_snr

__all__ = [
    "ccd_models",
]


def ccd_models() -> pylatex.Table:

    result = pylatex.Table()
    result.escape = False
    result._star_latex_name = True

    result.add_caption(
        pylatex.NoEscape(
            r"""
The sensor model parameters which best fit the measurements in \citet{Boerner2012}
and \citet{Heymes2020}."""
        )
    )
    result.append(pylatex.Label("table:models"))

    ccd = ccd_snr.ccd()
    ccd_aia = ccd_snr.ccd_aia()

    unit = u.nm
    unit_substrate = u.um

    with result.create(pylatex.Tabular("l|l|rrrrr")) as tabular:
        tabular.escape = False
        tabular.add_row(
            [
                "Source",
                "implementation",
                r"$\eta_0$",
                rf"$W$ ({unit:latex_inline})",
                rf"$\delta$ ({unit:latex_inline})",
                rf"$D$ ({unit_substrate:latex_inline})",
                rf"substrate roughness ({unit:latex_inline})",
            ]
        )
        tabular.add_hline()
        tabular.add_row(
            [
                "\citet{Boerner2012}",
                r"\href{https://optika.readthedocs.io/en/latest/_autosummary/optika.sensors.materials.e2v_ccd203.html}{\texttt{e2v\_ccd203}}",
                f"{ccd_aia.cce_backsurface:0.3f}",
                f"{ccd_aia.thickness_implant.to_value(unit):0.0f}",
                f"{ccd_aia.thickness_oxide.to_value(unit):0.1f}",
                f"{ccd_aia.thickness_substrate.to_value(unit_substrate):0.0f}",
                f"{ccd_aia.roughness_substrate.to_value(unit):0.1f}",
            ]
        )
        tabular.add_row(
            [
                "\citet{Heymes2020}",
                r"\href{https://optika.readthedocs.io/en/latest/_autosummary/optika.sensors.materials.e2v_ccd97.html}{\texttt{e2v\_ccd97}}",
                f"{ccd.cce_backsurface:0.3f}",
                f"{ccd.thickness_implant.to_value(unit):0.0f}",
                f"{ccd.thickness_oxide.to_value(unit):0.1f}",
                f"{ccd.thickness_substrate.to_value(unit_substrate):0.0f}",
                f"{ccd.roughness_substrate.to_value(unit):0.1f}",
            ]
        )

    return result
