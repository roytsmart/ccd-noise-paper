import astropy.units as u
import named_arrays as na
import optika

__all__ = [
    "vmr_stern",
]


def vmr_stern(
    wavelength: u.Quantity | na.AbstractScalar,
    temperature: u.Quantity | na.AbstractScalar,
) -> na.ScalarArray:
    """
    The variance-to-mean ratio (VMR) predicted by the Stern et al. (1986).

    Parameters
    ----------
    wavelength
        The wavelength of the incident light
    temperature
        The temperature of the light-sensitive silicon.
    """

    n = optika.sensors.quantum_yield_ideal(
        wavelength=wavelength,
        temperature=temperature,
    )

    F = optika.sensors.fano_factor(
        wavelength=wavelength,
        temperature=temperature,
    )

    result = n + F

    return result * u.ph
