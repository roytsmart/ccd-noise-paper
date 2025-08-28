import functools
import astropy.units as u
import optika

__all__ = [
    "ccd",
    "ccd_aia",
]


@functools.cache
def ccd() -> optika.sensors.E2VCCD97Material:
    return optika.sensors.E2VCCD97Material(temperature=190 * u.K)


@functools.cache
def ccd_aia() -> optika.sensors.E2VCCD203Material:
    return optika.sensors.E2VCCD203Material()
