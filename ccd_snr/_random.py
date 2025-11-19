import numpy as np
import named_arrays as na

__all__ = [
    "discrete_gamma",
]


def discrete_gamma(
    mean: float | na.ScalarArray,
    vmr: float | na.ScalarArray,
    shape_random: None | dict[str, int] = None,
) -> na.ScalarArray:

    x = na.random.gamma(
        shape=mean / vmr,
        scale=vmr,
        shape_random=shape_random,
    )

    x = np.where(
        condition=vmr != 0,
        x=x,
        y=mean,
    )

    unit_x = x.unit
    if unit_x is not None:
        x = x.value

    x_frac, x_int = np.modf(x)
    x_frac = na.random.binomial(
        n=1,
        p=x_frac,
        shape_random=shape_random,
    )
    x = x_int + x_frac

    if unit_x is not None:
        x = x << unit_x

    return x
