import numpy as np
import scipy.special
import astropy.units as u
import named_arrays as na


def _kernel_1d(
    width_diffusion: u.Quantity,
    width_pixel: u.Quantity,
    index_pixel: int | na.AbstractScalar,
) -> na.AbstractScalar:

    w = width_diffusion
    d = width_pixel
    n = index_pixel

    x = d / w
    x2 = np.square(x)

    c = 1 / (x * np.sqrt(2 * np.pi))

    def g(m: int | na.AbstractScalar) -> na.AbstractScalar:
        return np.exp(-x2 * m / 2)

    def e(m: int | na.AbstractScalar) -> na.AbstractScalar:
        return m * scipy.special.erf(x * m / np.sqrt(2))

    g1 = g(np.square(n - 1))
    g2 = -2 * g(np.square(n))
    g3 = g(np.square(n + 1))

    e1 = e(n - 1) / 2
    e2 = -e(n)
    e3 = e(n + 1) / 2

    result = c * (g1 + g2 + g3) + e1 + e2 + e3

    return result


def _kernel_2d(
    width_diffusion: u.Quantity,
    width_pixel: u.Quantity,
    index_x: int | na.AbstractScalar,
    index_y: int | na.AbstractScalar,
) -> na.AbstractScalar:

    kx = _kernel_1d(
        width_diffusion=width_diffusion,
        width_pixel=width_pixel,
        index_pixel=index_x,
    )
    print(f"{kx=}")
    ky = _kernel_1d(
        width_diffusion=width_diffusion,
        width_pixel=width_pixel,
        index_pixel=index_y,
    )

    return kx * ky


def diffusion_kernel(
    width_diffusion: u.Quantity,
    width_pixel: u.Quantity,
) -> na.FunctionArray:
    """
    The charge diffusion kernel convolved with a pixel.

    Parameters
    ----------
    width_diffusion
        The standard deviation of the charge diffusion kernel.
    width_pixel
        The width of a pixel.
    """

    index_x = na.linspace(-1, 1, axis="kx", num=3)
    index_y = na.linspace(-1, 1, axis="ky", num=3)

    output = _kernel_2d(
        width_diffusion=width_diffusion,
        width_pixel=width_pixel,
        index_x=index_x,
        index_y=index_y,
    )

    return na.FunctionArray(
        inputs=na.Cartesian2dVectorArray(index_x, index_y),
        outputs=output,
    )
