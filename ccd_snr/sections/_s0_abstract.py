import aastex

__all__ = [
    "abstract",
]


def abstract() -> aastex.Abstract:
    result = aastex.Abstract()
    result.append(r"""
Ultraviolet (\acs{UV}) astronomy currently relies on back-illuminated silicon imaging sensors.
While the noise in these sensors is typically assumed to be dominated by photon shot noise,
measurements from \WFC\ and \IRIS\ reveal a significant discrepancy:
the noise measured in the \UV\ is systematically lower than theoretical predictions.
We propose that this discrepancy is caused by \PCC,
whereby a fraction of photogenerated electron-hole pairs recombine before they can be measured.
We present a simple theoretical model,
valid for wavelengths from \qtyrange{1}{10000}{\angstrom},
that incorporates the effects of \PCC\
and shows better agreement with the noise measurements from both \WFC\ and \IRIS,
resolving the previously unexplained discrepancy.
This finding implies that the signal-to-noise ratio achievable with these sensors
is higher in the \UV\ than previously understood,
potentially impacting both future instrument proposals and the uncertainties of our current \UV\ imagery.
At about \qtyrange{2000}{3500}{\angstrom}, \PCC\ is the dominant noise source in the high-signal limit.
\acresetall""")
    return result
