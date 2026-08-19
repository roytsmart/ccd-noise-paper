import numpy as np
import astropy.units as u
import aastex
import named_arrays as na
import ccd_snr
from ccd_snr.instruments._util import _vmr_electron

__all__ = [
    "vmr_measured",
]


def vmr_measured() -> str:

    index_uv = dict(wavelength=slice(None, ~0))
    index_visible = dict(wavelength=~0)

    wavelength_iris = [
        1350 * u.AA,
        # the onboard blue LED used by \citet{Wulser2018} to measure the
        # visible-light gain, 430 nm for the SXI flight units \citep{Stern2004}
        4300 * u.AA,
    ]
    wavelength_iris = na.ScalarArray(
        ndarray=u.Quantity(wavelength_iris),
        axes="wavelength",
    )
    wavelength_wfc3 = ccd_snr.instruments.wfc3.wavelength

    vmr_iris = _vmr_electron(
        wavelength=wavelength_iris,
        width_pixel=ccd_snr.instruments.iris.width_pixel,
    )

    vmr_wfc3 = _vmr_electron(
        wavelength=wavelength_wfc3,
        width_pixel=ccd_snr.instruments.wfc3.width_pixel,
    )

    ratio_model_iris = vmr_iris[index_uv] / vmr_iris[index_visible]
    ratio_model_wfc3 = vmr_wfc3[index_uv] / vmr_wfc3[index_visible]

    ratio_measured_iris = [
        1.5,
    ]
    ratio_measured_wfc3 = [
        (1.093 + 1.093) / 2,
        (1.080 + 1.097) / 2,
        (1.065 + 1.072) / 2,
        (1.040 + 1.045) / 2,
        (1.044 + 1.026) / 2,
        (1.027 + 1.035) / 2,
        (1.012 + 1.016) / 2,
    ]

    ratio_measured_iris = np.array(ratio_measured_iris)
    ratio_measured_wfc3 = np.array(ratio_measured_wfc3)

    ratio_measured_iris = na.ScalarArray(ratio_measured_iris, axes="wavelength")
    ratio_measured_wfc3 = na.ScalarArray(ratio_measured_wfc3, axes="wavelength")

    # result = ""
    result = f"""{aastex.Variable("modeledIrisRatio", np.round(ratio_model_iris.ndarray[0].value, decimals=2)).dumps()}
{aastex.Variable("modeledWfcRatio", np.round(ratio_model_wfc3.ndarray[0].value, decimals=2)).dumps()}
{aastex.Variable("measuredIrisRatio", ratio_measured_iris.ndarray[0]).dumps()}
{aastex.Variable("measuredWfcRatio", np.round(ratio_measured_wfc3.ndarray[0], decimals=2)).dumps()}
{aastex.Variable("wavelengthIrisRatio", wavelength_iris.ndarray[0]).dumps()}
{aastex.Variable("wavelengthWfcRatio", wavelength_wfc3.ndarray[0].to(u.AA)).dumps()}
"""

    result += r"""\begin{deluxetable}{lrrrr}
\tablecaption{
\label{table:measurements}
The ratio of the \VMR\ of a \UV\ flat-field image to the \VMR\ of a
visible-light flat-field image.
The second column from the right is the value of this ratio
measured by \citet{Borders2010} and \citet{Wulser2018}.
For \IRIS\ this is the ratio of the inverse camera gains measured from
photon-transfer curves, 12 photons per data number using a deuterium lamp at
\qty{1350}{\angstrom} and 18 photons per data number using the onboard blue
light-emitting diode \citep{Wulser2018}, which we take to be the
\qty{430}{\nano\meter} device flown on the GOES Soft X-ray Imager
\citep{Stern2004}.
The rightmost column is the value of this quantity predicted by our
noise model (including charge diffusion).
}
"""

    result += rf"""\tablehead{{
\colhead{{Instrument}}
& \colhead{{$\lambda_\text{{UV}}$ ({u.AA:latex_inline})}}
& \colhead{{$\lambda_\text{{vis}}$ ({u.AA:latex_inline})}}
& \colhead{{measurement}}
& \colhead{{model}}
}}
"""
    result += "\\startdata\n"

    for i, index in enumerate(ratio_model_iris.ndindex()):
        instrument = r"\IRIS" if i == 0 else ""
        row = [
            instrument,
            f"{wavelength_iris[index].ndarray.to_value(u.AA):.0f}",
            f"{wavelength_iris[index_visible].ndarray.to_value(u.AA):.0f}",
            f"{ratio_measured_iris[index].ndarray:.2f}",
            f"{ratio_model_iris[index].ndarray:.2f}",
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
            f"{ratio_measured_wfc3[index].ndarray:.2f}",
            f"{ratio_model_wfc3[index].ndarray:.2f}",
        ]
        result += f"{'&'.join(row)} \\\\\n"

    result += "\\enddata\n"
    result += "\\end{deluxetable}"

    return result
