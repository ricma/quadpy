# -*- coding: utf-8 -*-
#
from __future__ import division

import sympy

from ._helpers import concat, zero, symm_r0, symm_s, QuadrilateralScheme
from ..helpers import article


citation = article(
    authors=["J.C.P. Miller"],
    title="Numerical Quadrature Over a Rectangular Domain in Two or More Dimensions. Part 3: Quadrature of a Harmonic Integrand",
    journal="Mathematics of Computation",
    volume="14",
    number="71",
    month="jul",
    year="1960",
    pages="240-248",
    url="https://doi.org/10.2307/2003163",
)


def miller(symbolic=False):
    frac = sympy.Rational if symbolic else lambda x, y: x / y

    weights, points = concat(
        zero(frac(250, 225)), symm_r0([-frac(8, 225), 1]), symm_s([frac(7, 900), 1])
    )
    weights *= 4
    # This scheme is exact for _harmonic_ integrands of degree <= 11.
    return QuadrilateralScheme("Miller", weights, points, 1, citation)