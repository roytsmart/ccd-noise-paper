import astropy.units as u
import numpy as np

import aastex
import named_arrays as na
import optika
import ccd_snr

__all__ = [
    "measurements",
]


def measurements() -> str:

    ccd = ccd_snr.ccd()

    num_x = 1000
    num_y = 1000
    axis_experiment = ("detector_x", "detector_y")
    shape_experiment = dict(detector_x=num_x, detector_y=num_y)

    intensity = na.broadcast_to(100 * u.ph, shape_experiment)
    direction = na.Cartesian3dVectorArray(0, 0, 1)
    normal = na.Cartesian3dVectorArray(0, 0, -1)

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

    rays_iris = optika.rays.RayVectorArray(
        intensity=intensity,
        wavelength=wavelength_iris,
        direction=direction,
    )
    rays_wfc3 = optika.rays.RayVectorArray(
        intensity=intensity,
        wavelength=wavelength_wfc3,
        direction=direction,
    )

    electrons_iris = ccd.signal(rays_iris, normal).intensity
    electrons_wfc3 = ccd.signal(rays_wfc3, normal).intensity

    kernel_iris = ccd_snr.diffusion.kernel(
        wavelength=wavelength_iris,
        width_pixel=ccd_snr.instruments.iris.width_pixel,
    )
    kernel_wfc3 = ccd_snr.diffusion.kernel(
        wavelength=wavelength_wfc3,
        width_pixel=ccd_snr.instruments.wfc3.width_pixel,
    )

    electrons_iris = na.convolve(
        array=electrons_iris,
        kernel=kernel_iris.outputs,
        axis=axis_experiment,
    )
    electrons_wfc3 = na.convolve(
        array=electrons_wfc3,
        kernel=kernel_wfc3.outputs,
        axis=axis_experiment,
    )

    vmr_iris = electrons_iris.vmr(axis_experiment)
    vmr_wfc3 = electrons_wfc3.vmr(axis_experiment)

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
{aastex.Variable("wavelengthWfcRatio", wavelength_wfc3.ndarray[0]).dumps()}
"""

    result += r"""\begin{deluxetable}{lrrrr}
\tablecaption{
\label{table:measurements}
The ratio of the \VMR\ in \UV\ to the \VMR\ in visible light for instruments
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
