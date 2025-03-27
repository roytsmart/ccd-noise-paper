import astropy.units as u
import numpy as np
import named_arrays as na
import ccd_snr
from ccd_snr.instruments._util import _fano_electron

__all__ = [
    "measurements",
]


def measurements() -> str:

    index_uv = dict(wavelength=slice(None, ~0))
    index_visible = dict(wavelength=~0)

    wavelength_iris = [
        1350 * u.AA,
        4500 * u.AA,
    ]
    wavelength_iris = na.ScalarArray(
        ndarray=u.Quantity(wavelength_iris),
        axes="wavelength",
    )
    wavelength_wfc3 = ccd_snr.instruments.wfc3.wavelength

    fano_electrons_iris = _fano_electron(wavelength_iris)
    fano_electrons_wfc3 = ccd_snr.instruments.wfc3.fano_electron

    ratio_model_iris = fano_electrons_iris / fano_electrons_iris[index_visible]
    ratio_model_wfc3 = fano_electrons_wfc3 / fano_electrons_wfc3[index_visible]

    ratio_model_iris = ratio_model_iris[index_uv]
    ratio_model_wfc3 = ratio_model_wfc3[index_uv]

    ratio_measured_iris = [
        1.5,
    ]
    ratio_measured_wfc3 = [
        1.07,
        1.08,
        1.04,
        1.00,
    ]

    ratio_measured_iris = np.array(ratio_measured_iris)
    ratio_measured_wfc3 = np.array(ratio_measured_wfc3)

    ratio_measured_iris = na.ScalarArray(ratio_measured_iris, axes="wavelength")
    ratio_measured_wfc3 = na.ScalarArray(ratio_measured_wfc3, axes="wavelength")

    result = r"""\begin{deluxetable}{lrrrr}
\tablecaption{
\label{table:measurements}
The ratio of the \VSR\ in \UV\ to the \VSR\ in visible light for instruments
which this data is available.
}
"""

    result += rf"""\tablehead{{
\colhead{{Instrument}}
& \colhead{{$\lambda_\text{{UV}}$ ({u.AA:latex_inline})}}
& \colhead{{$\lambda_\text{{vis}}$ ({u.AA:latex_inline})}}
& \colhead{{model}}
& \colhead{{measurement}}
}}
"""
    result += "\\startdata\n"

    for i, index in enumerate(ratio_model_iris.ndindex()):
        if i == 0:
            instrument = r"\IRIS"
        else:
            instrument = ""
        row = [
            instrument,
            f"{wavelength_iris[index].ndarray.to_value(u.AA):.0f}",
            f"{wavelength_iris[index_visible].ndarray.to_value(u.AA):.0f}",
            f"{ratio_model_iris[index].ndarray:.2f}",
            f"{ratio_measured_iris[index].ndarray:.2f}",
        ]
        result += f"{'&'.join(row)} \\\\\n"

    result += "\\tableline\n"

    for i, index in enumerate(ratio_model_wfc3.ndindex()):
        if i == 0:
            instrument = r"WFC3"
        else:
            instrument = ""
        row = [
            instrument,
            f"{wavelength_wfc3[index].ndarray.to_value(u.AA):.0f}",
            f"{wavelength_wfc3[index_visible].ndarray.to_value(u.AA):.0f}",
            f"{ratio_model_wfc3[index].ndarray:.2f}",
            f"{ratio_measured_wfc3[index].ndarray:.2f}",
        ]
        result += f"{'&'.join(row)} \\\\\n"

    result += "\\enddata\n"
    result += "\\end{deluxetable}"

    return result
