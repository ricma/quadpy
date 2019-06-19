# -*- coding: utf-8 -*-
#
from __future__ import print_function

import numpy
import pytest
import sympy

import orthopy
import quadpy
from quadpy.quadrilateral import Product

from helpers import check_degree_ortho


def _integrate_exact(f, quadrilateral):
    xi = sympy.DeferredVector("xi")
    pxi = (
        quadrilateral[0] * 0.25 * (1.0 + xi[0]) * (1.0 + xi[1])
        + quadrilateral[1] * 0.25 * (1.0 - xi[0]) * (1.0 + xi[1])
        + quadrilateral[2] * 0.25 * (1.0 - xi[0]) * (1.0 - xi[1])
        + quadrilateral[3] * 0.25 * (1.0 + xi[0]) * (1.0 - xi[1])
    )
    pxi = [sympy.expand(pxi[0]), sympy.expand(pxi[1])]
    # determinant of the transformation matrix
    det_J = +sympy.diff(pxi[0], xi[0]) * sympy.diff(pxi[1], xi[1]) - sympy.diff(
        pxi[1], xi[0]
    ) * sympy.diff(pxi[0], xi[1])
    # we cannot use abs(), see <https://github.com/sympy/sympy/issues/4212>.
    abs_det_J = sympy.Piecewise((det_J, det_J >= 0), (-det_J, det_J < 0))

    g_xi = f(pxi)

    exact = sympy.integrate(
        sympy.integrate(abs_det_J * g_xi, (xi[1], -1, 1)), (xi[0], -1, 1)
    )
    return float(exact)


def _integrate_exact2(k, x0, x1, y0, y1):
    return (
        1.0
        / (k[0] + 1)
        * (x1 ** (k[0] + 1) - x0 ** (k[0] + 1))
        * 1.0
        / (k[1] + 1)
        * (y1 ** (k[1] + 1) - y0 ** (k[1] + 1))
    )


@pytest.mark.parametrize(
    "scheme,tol",
    [(quadpy.quadrilateral.albrecht_collatz_1(), 1.0e-14) for k in [1, 2, 3, 4]]
    + [(quadpy.quadrilateral.albrecht_collatz_2(), 1.0e-14) for k in [1, 2, 3, 4]]
    + [(quadpy.quadrilateral.albrecht_collatz_3(), 1.0e-14) for k in [1, 2, 3, 4]]
    + [(quadpy.quadrilateral.albrecht_collatz_4(), 1.0e-14) for k in [1, 2, 3, 4]]
    + [(quadpy.quadrilateral.cohen_gismalla_1(), 1.0e-6)]
    + [(quadpy.quadrilateral.cohen_gismalla_2(), 1.0e-6)]
    + [(quadpy.quadrilateral.cools_haegemans_1985_1(), 1.0e-10)]
    + [(quadpy.quadrilateral.cools_haegemans_1985_2(), 1.0e-10)]
    + [(quadpy.quadrilateral.cools_haegemans_1985_3(), 1.0e-10)]
    + [(quadpy.quadrilateral.CoolsHaegemans1988[k](), 1.0e-14) for k in [1, 2]]
    + [(scheme(), 1.0e-13) for scheme in quadpy.quadrilateral.Dunavant.values()]
    + [(quadpy.quadrilateral.franke_1(lmbda), 1.0e-13) for lmbda in [0.0, 1.0, -0.8]]
    + [
        (scheme(), 1.0e-13)
        for scheme in [
            quadpy.quadrilateral.franke_2a,
            quadpy.quadrilateral.franke_2b,
            quadpy.quadrilateral.franke_3a,
            quadpy.quadrilateral.franke_3b,
            quadpy.quadrilateral.franke_3c,
            quadpy.quadrilateral.franke_5,
            quadpy.quadrilateral.franke_6,
            quadpy.quadrilateral.franke_8,
        ]
    ]
    + [(quadpy.quadrilateral.HammerStroud[k](), 1.0e-14) for k in ["1-2", "2-2", "3-2"]]
    + [(quadpy.quadrilateral.MorrowPatterson[k](), 1.0e-5) for k in [1, 2]]
    + [
        (quadpy.quadrilateral.Stroud[k](), 1.0e-13)
        for k in quadpy.quadrilateral.Stroud.keys()
    ]
    # + [
    #     (quadpy.quadrilateral.StroudN(k), 1.0e-14)
    #     for k in [
    #         "Cn 1-1",
    #         "Cn 1-2",
    #         "Cn 2-1",
    #         "Cn 2-2",
    #         "Cn 3-1",
    #         "Cn 3-2",
    #         "Cn 3-3",
    #         "Cn 3-4",
    #         "Cn 3-5",
    #         "Cn 3-6",
    #         "Cn 5-2",
    #         "Cn 5-3",
    #         "Cn 5-4",
    #         "Cn 5-5",
    #         "Cn 5-6",
    #         "Cn 5-7",
    #         "Cn 5-9",
    #         "cn 7-1"
    #     ]
    # ]
    + [(quadpy.quadrilateral.HaegemansPiessens(), 1.0e-14)]
    + [(quadpy.quadrilateral.PiessensHaegemans[k](), 1.0e-14) for k in [1, 2]]
    # TODO better-quality points/weights for Schmidt
    + [(quadpy.quadrilateral.Schmid[k](), 1.0e-10) for k in [2, 4, 6]]
    + [(scheme(), 1.0e-13) for scheme in quadpy.quadrilateral.Sommariva.values()]
    + [(quadpy.quadrilateral.Waldron(0.6, numpy.pi / 7), 1.0e-14)]
    + [(scheme(), 1.0e-14) for scheme in quadpy.quadrilateral.WissmannBecker.values()]
    + [(scheme(), 1.0e-14) for scheme in quadpy.quadrilateral.WitherdenVincent.values()]
    + [(Product(quadpy.line_segment.Midpoint()), 1.0e-14)]
    + [(Product(quadpy.line_segment.Trapezoidal()), 1.0e-14)]
    + [(Product(quadpy.line_segment.GaussLegendre(k)), 1.0e-14) for k in range(1, 5)]
    + [
        (Product(quadpy.line_segment.NewtonCotesClosed(k)), 1.0e-14)
        for k in range(1, 5)
    ]
    + [(Product(quadpy.line_segment.NewtonCotesOpen(k)), 1.0e-14) for k in range(6)],
)
def test_scheme(scheme, tol):
    # Test integration until we get to a polynomial degree `d` that can no
    # longer be integrated exactly. The scheme's degree is `d-1`.
    print(scheme.name)
    assert scheme.points.dtype in [numpy.float64, numpy.int64], scheme.name
    assert scheme.weights.dtype in [numpy.float64, numpy.int64], scheme.name

    def eval_orthopolys(x):
        return numpy.concatenate(
            orthopy.quadrilateral.tree(x, scheme.degree + 1, symbolic=False)
        )

    quad = quadpy.quadrilateral.rectangle_points([-1.0, +1.0], [-1.0, +1.0])
    vals = scheme.integrate(eval_orthopolys, quad)
    # Put vals back into the tree structure:
    # len(approximate[k]) == k+1
    approximate = [
        vals[k * (k + 1) // 2 : (k + 1) * (k + 2) // 2]
        for k in range(scheme.degree + 2)
    ]

    exact = [numpy.zeros(k + 1) for k in range(scheme.degree + 2)]
    exact[0][0] = 2.0

    degree = check_degree_ortho(approximate, exact, abs_tol=tol)

    assert degree >= scheme.degree, "Observed: {}, expected: {}".format(
        degree, scheme.degree
    )
    return


@pytest.mark.parametrize("scheme", [Product(quadpy.line_segment.GaussLegendre(5))])
def test_show(scheme):
    quadpy.quadrilateral.show(scheme)
    return


if __name__ == "__main__":
    # scheme_ = Product(quadpy.line_segment.GaussLegendre(6))
    # scheme_ = quadpy.quadrilateral.HammerStroud("3-2")
    scheme_ = quadpy.quadrilateral.Stroud["C2 3-2"]()
    test_show(scheme_)
    test_scheme(scheme_, 1.0e-14)
