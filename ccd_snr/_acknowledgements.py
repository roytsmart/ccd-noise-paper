__all__ = [
    "acknowledgements",
]


def acknowledgements() -> str:
    return r"""\begin{acknowledgements}
    This work has been supported by the
    Lockheed Martin subcontract 8100002702 for the NASA/IRIS small explorer mission,
    and NASA grants 
    
    NASA grants XXXX, XXXX and XXXX.
    This article is an example of an executable paper \citep{Lasser2020},
    all of the simulations, figures, and tables are generated dynamically
    when this article is created.
    This helps prevent mistakes and allows this research to be as repeatable as possible.
    The code to create this document is available at 
    \url{https://github.com/roytsmart/ccd-noise-paper}.
\end{acknowledgements}
"""
