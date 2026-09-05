import aastex

__all__ = [
    "acronyms",
]


def acronyms() -> list[aastex.Acronym]:
    """
    A list of acronyms that are used in the body of the article.
    """
    return [
        aastex.Acronym("CCD", "charge-coupled device", plural=True),
        aastex.Acronym("CMOS", "complementary metal–oxide–semiconductor"),
        aastex.Acronym("UV", "ultraviolet"),
        aastex.Acronym("NUV", "near ultraviolet"),
        aastex.Acronym("FUV", "far ultraviolet"),
        aastex.Acronym("EUV", "extreme ultraviolet"),
        aastex.Acronym("SXR", "soft X-ray"),
        aastex.Acronym("IR", "infrared"),
        aastex.Acronym("QE", "quantum efficiency"),
        aastex.Acronym("QY", "quantum yield"),
        aastex.Acronym("CCE", "charge-collection efficiency"),
        aastex.Acronym("SNR", "signal-to-noise ratio"),
        aastex.Acronym("SDO", "NASA's Solar Dynamics Observatory"),
        aastex.Acronym("AIA", "the Atmospheric Imaging Assembly"),
        aastex.Acronym("IRIS", "the Interface Region Imaging Spectrograph"),
        aastex.Acronym("SJI", "the Slit-Jaw Imager"),
        aastex.Acronym("SAA", "the South Atlantic Anomaly"),
        aastex.Acronym("MUSE", "the Multi-slit Solar Explorer"),
        aastex.Acronym("WFC", "HST's Wide Field Camera 3", name_short="WFC3"),
        aastex.Acronym("PCC", "partial charge collection"),
        aastex.Acronym("CCC", "complete-charge-collection"),
        aastex.Acronym("VMR", "variance-to-mean ratio"),
        aastex.Acronym("PDF", "probability distribution function"),
        aastex.Acronym("PMF", "probability mass function", plural=True),
        aastex.Acronym("MCC", "mean charge capture"),
        aastex.Acronym("PyPI", "the Python Package Index"),
        aastex.Acronym("ESIS", "the EUV Snapshot Imaging Spectrograph"),
        aastex.Acronym("FURST", "the Full-sun Ultraviolet Rocket Spectrometer"),
    ]
