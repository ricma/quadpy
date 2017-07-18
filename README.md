# quadpy

Your one-stop shop for numerical integration in Python.

[![Build Status](https://travis-ci.org/nschloe/quadpy.svg?branch=master)](https://travis-ci.org/nschloe/quadpy)
[![codecov](https://codecov.io/gh/nschloe/quadpy/branch/master/graph/badge.svg)](https://codecov.io/gh/nschloe/quadpy)
[![PyPi Version](https://img.shields.io/pypi/v/quadpy.svg)](https://pypi.python.org/pypi/quadpy)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/quadpy.svg?style=social&label=Stars&maxAge=2592000)](https://github.com/nschloe/quadpy)

Hundreds of numerical integration schemes for line segments, circles, disks,
triangles, quadrilaterals, spheres, tetrahedra, hexahedra, wedges, pyramids.

To numerically integrate any function over any given triangle, do
```python
import numpy
import quadpy

def f(x):
    return numpy.sin(x[0]) * numpy.sin(x[1])

triangle = numpy.array([[0.0, 0.0], [1.0, 0.0], [0.7, 0.5]])

val = quadpy.triangle.integrate(f, triangle, quadpy.triangle.Strang(9))
```
This uses Strang's rule of degree 6.

quadpy is fully vectorized, so if you like to compute the integral of a
function on many domains at once, you can provide them all in one `integrate()`
call, e.g.,
```python
triangles = numpy.array([
    [[0.0, 0.0], [1.2, 0.6], [26.0, 31.0], [0.1, 0.3], [8.6, 6.0]],
    [[1.0, 0.0], [1.3, 0.7], [24.0, 27.0], [0.4, 0.4], [9.4, 5.6]],
    [[0.0, 1.0], [1.4, 0.8], [33.0, 28.0], [0.7, 0.1], [7.5, 7.4]],
    ])
```
The same goes for functions with vectorized output, e.g.,
```python
def f(x):
    return [numpy.sin(x[0]), numpy.sin(x[1])]
```

More examples under [test/examples_test.py](https://github.com/nschloe/quadpy/blob/master/test/examples_test.py).

### Adaptive quadrature

quadpy can do adaptive quadrature for certain domains.
Again, everything is fully vectorized, so you can provide multiple intervals
and vector-valued functions.

#### Line segments
```python
val, error_estimate = quadpy.line_segment.adaptive_integrate(
        lambda x: x * sin(5 * x),
        [0.0, pi],
        1.0e-10
        )
```

#### Triangles
```python
val, error_estimate = quadpy.triangle.adaptive_integrate(
        lambda x: x[0] * sin(5 * x[1]),
        [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]],
        1.0e-10
        )
```
_ProTip:_ You can provide many triangles that together form a domain to get an
approximation of the integral over the domain.

## Schemes

### Line segment
<img src="https://nschloe.github.io/quadpy/line.png" width="50%">

 * Chebyshev-Gauss (both variants, arbitrary degree)
 * Clenshaw-Curtis (after
   [Waldvogel](https://dx.doi.org/10.1007/s10543-006-0045-4), arbitrary degree)
 * Fejér-type-1 (after
   [Waldvogel](https://dx.doi.org/10.1007/s10543-006-0045-4), arbitrary degree)
 * Fejér-type-2 (after
   [Waldvogel](https://dx.doi.org/10.1007/s10543-006-0045-4), arbitrary degree)
 * Gauss-Hermite (via
   [NumPy](https://docs.scipy.org/doc/numpy/reference/generated/numpy.polynomial.hermite.hermgauss.html), arbitrary degree)
 * Gauss-Laguerre (via
   [NumPy](https://docs.scipy.org/doc/numpy/reference/generated/numpy.polynomial.laguerre.laggauss.html), arbitrary degree)
 * Gauss-Legendre (via
   [NumPy](https://docs.scipy.org/doc/numpy/reference/generated/numpy.polynomial.legendre.leggauss.html), arbitrary degree)
 * Gauss-Lobatto (arbitrary degree)
 * Gauss-Kronrod (after [Laurie](https://doi.org/10.1090/S0025-5718-97-00861-2), arbitrary degree)
 * [Gauss-Patterson](https://doi.org/10.1090/S0025-5718-68-99866-9) (7 schemes up to degree 191)
 * Gauss-Radau (arbitrary degree)
 * closed Newton-Cotes (arbitrary degree)
 * open Newton-Cotes (arbitrary degree)

Example:
```python
val = quadpy.line_segment.integrate(
    lambda x: numpy.exp(x),
    [0.0, 1.0],
    quadpy.line_segment.GaussPatterson(5)
    )
```

### Circle
<img src="https://nschloe.github.io/quadpy/circle.png" width="25%">

 * equidistant points

Example:
```python
val = quadpy.circle.integrate(
    lambda x: numpy.exp(x[0]),
    [0.0, 0.0], 1.0,
    quadpy.circle.Equidistant(7)
    )
```

### Triangle
<img src="https://nschloe.github.io/quadpy/triangle.png" width="25%">

Apart from the classical centroid, vertex, and seven-point schemes we have

 * [Hammer-Marlowe-Stroud](https://doi.org/10.1090/S0025-5718-1956-0086389-6)
   (1956, 5 schemes up to degree 5),
 * open and closed Newton-Cotes schemes (1970, after [Silvester](https://doi.org/10.1090/S0025-5718-1970-0258283-6), arbitrary degree),
 * [Stroud](https://books.google.de/books/about/Approximate_calculation_of_multiple_inte.html?id=L_tQAAAAMAAJ&redir_esc=y) (1971, 10 schemes up to degree 5)
 * [Strang](http://bookstore.siam.org/wc08/)/[Cowper](https://dx.doi.org/10.1002/nme.1620070316) (1973, 10 schemes up to
   degree 7),
 * [Lyness-Jespersen](https://dx.doi.org/10.1093/imamat/15.1.19) (1975, 21
   schemes up to degree 11),
 * [Hillion](https://dx.doi.org/10.1002/nme.1620110504) (1977),
 * [Grundmann-Möller](http://dx.doi.org/10.1137/0715019) (1978, arbitrary degree),
 * [Laursen-Gellert](https://dx.doi.org/10.1002/nme.1620120107) (1978, 17
   schemes up to degree 10),
 * [CUBTRI](http://dl.acm.org/citation.cfm?id=356001) (Laurie, 1982, degree 8),
 * [TRIEX](http://dl.acm.org/citation.cfm?id=356070) (de Doncker-Robinson, 1984, degrees 9 and 11),
 * [Dunavant](https://dx.doi.org/10.1002/nme.1620210612) (1985, 20 schemes up
   to degree 20),
 * [Cools-Haegemans](https://lirias.kuleuven.be/handle/123456789/131869) (1987,
   degrees 8 and 11),
 * [Gatermann](https://dx.doi.org/10.1007/BF02251251) (1988, degree 7)
 * Berntsen-Espelid (1990, 4 schemes of degree 13, the first one being
   [DCUTRI](http://dl.acm.org/citation.cfm?id=131772)),
 * [Liu-Vinokur](https://dx.doi.org/10.1006/jcph.1998.5884) (1998, 13 schemes
   up to degree 5),
 * [Walkington](http://www.math.cmu.edu/~nw0z/publications/00-CNA-023/023abs/)
   (2000, 5 schemes up to degree 5),
 * [Wandzura-Xiao](https://dx.doi.org/10.1016/S0898-1221(03)90004-6) (2003, 6
   schemes up to degree 30),
 * [Taylor-Wingate-Bos](https://arxiv.org/abs/math/0501496) (2005, 5 schemes up
   to degree 14),
 * [Zhang-Cui-Liu](http://www.jstor.org/stable/43693493) (2009, 3 schemes up to
   degree 20),
 * [Xiao-Gimbutas](http://dx.doi.org/10.1016/j.camwa.2009.10.027) (2010, 50
   schemes up to degree 50),
 * [Vioreanu-Rokhlin](https://doi.org/10.1137/110860082) (2014, 20
   schemes up to degree 62),
 * [Willams-Shunn-Jameson](https://doi.org/10.1016/j.cam.2014.01.007) (2014, 8
   schemes up to degree 12).

Example:
```python
val = quadpy.triangle.integrate(
    lambda x: numpy.exp(x[0]),
    [[0.0, 0.0], [1.0, 0.0], [0.5, 0.7]],
    quadpy.triangle.XiaoGimbutas(5)
    )
```

### Disk
<img src="https://nschloe.github.io/quadpy/disk.png" width="25%">

 * [Peirce](http://www.jstor.org/stable/2098722) (1957, arbitrary degree)
 * [Lether](http://www.jstor.org/stable/2949473) (1971, arbitrary degree)
 * [Cools-Haegemans](https://lirias.kuleuven.be/handle/123456789/131870) (1985, 3 schemes up to degree 9)
 * [Cools-Kim](https://link.springer.com/article/10.1007/BF03012263) (2000, 3 schemes up to degree 21)

Example:
```python
val = quadpy.disk.integrate(
    lambda x: numpy.exp(x[0]),
    [0.0, 0.0], 1.0,
    quadpy.disk.Lether(6)
    )
```

### Quadrilateral
<img src="https://nschloe.github.io/quadpy/quad.png" width="25%">

 * Product schemes derived from line segment schemes
 * [Stroud](https://books.google.de/books/about/Approximate_calculation_of_multiple_inte.html?id=L_tQAAAAMAAJ&redir_esc=y) (1971, 11 schemes up to degree 15)
 * [Cools-Haegemans](https://lirias.kuleuven.be/handle/123456789/131870) (1985, 3 schemes up to degree 13)
 * [Dunavant](https://dx.doi.org/10.1002/nme.1620211004) (1985, 11 schemes up to degree 19)

Example:
```python
val = quadpy.quadrilateral.integrate(
    lambda x: numpy.exp(x[0]),
    [[0.0, 0.0], [1.0, 0.0], [0.5, 0.7], [0.3, 0.9]],
    quadpy.quadrilateral.Stroud(6)
    )
```

### Tetrahedron
<img src="https://nschloe.github.io/quadpy/tet.png" width="25%">

 * [Hammer-Marlowe-Stroud](https://doi.org/10.1090/S0025-5718-1956-0086389-6)
   (1956, 3 schemes up to degree 3)
 * open and closed Newton-Cotes (1970, after [Silvester](https://doi.org/10.1090/S0025-5718-1970-0258283-6)) (arbitrary degree)
 * [Stroud](https://cds.cern.ch/record/104291?ln=en) (1971, 2 schemes up to
   degree 3)
 * [Grundmann-Möller](http://dx.doi.org/10.1137/0715019) (1978, arbitrary degree),
 * [Yu](http://dx.doi.org/10.1016/0045-7825(84)90072-0) (1984, 5 schemes up to degree 6)
 * [Keast](http://dx.doi.org/10.1016/0045-7825(86)90059-9) (1986, 11 schemes up to
   degree 8)
 * [Gatermann](https://dx.doi.org/10.1007/978-94-011-2646-5_2) (1992, degree 5)
 * [Beckers-Haegemans](https://lirias.kuleuven.be/handle/123456789/132648) (1990, degrees 8 and 9)
 * [Liu-Vinokur](http://dx.doi.org/10.1006/jcph.1998.5884) (1998, 14 schemes up to
   degree 5)
 * [Walkington](http://www.math.cmu.edu/~nw0z/publications/00-CNA-023/023abs/)
   (2000, 6 schemes up to degree 7),
 * [Zienkiewicz](http://www.sciencedirect.com/science/book/9780750664318)
   (2005, 2 schemes up to degree 3)
 * [Zhang-Cui-Liu](http://www.jstor.org/stable/43693493) (2009, 2 schemes up to
   degree 14)
 * [Xiao-Gimbutas](http://dx.doi.org/10.1016/j.camwa.2009.10.027) (2010, 15
   schemes up to degree 15)
 * [Shunn-Ham](http://dx.doi.org/10.1016/j.cam.2012.03.032) (2012, 6 schemes up to
   degree 7)
 * [Vioreanu-Rokhlin](https://doi.org/10.1137/110860082) (2014, 10
   schemes up to degree 13),
 * [Willams-Shunn-Jameson](https://doi.org/10.1016/j.cam.2014.01.007) (2014, 1
   scheme with degree 9)

Example:
```python
val = quadpy.tetrahedron.integrate(
    lambda x: numpy.exp(x[0]),
    [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.7, 0.0], [0.3, 0.9, 1.0]],
    quadpy.tetrahedron.Keast(10)
    )
```

### Hexahedron
<img src="https://nschloe.github.io/quadpy/hexa.png" width="25%">

 * Product schemes derived from line segment schemes

Example:
```python
val = quadpy.hexahedron.integrate(
    lambda x: numpy.exp(x[0]),
    [
      [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.7, 0.0], [0.3, 0.9, 0.0],
      [0.0, 0.1, 1.0], [0.7, 0.1, 1.0], [0.4, 0.6, 1.0], [0.2, 1.0, 1.0],
    ],
    quadpy.hexahedron.Product(quadpy.line_segment.NewtonCotesClosed(3))
    )
```

### Pyramid
<img src="https://nschloe.github.io/quadpy/pyra.png" width="25%">

 * [Felippa's schemes](http://dx.doi.org/10.1108/02644400410554362) (9 schemes
   up to degree 5)

Example:
```python
val = quadpy.pyramid.integrate(
    lambda x: numpy.exp(x[0]),
    [
      [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.7, 0.0], [0.3, 0.9, 0.0],
      [0.0, 0.1, 1.0],
    ],
    quadpy.pyramid.Felippa(5)
    )
```

### Wedge
<img src="https://nschloe.github.io/quadpy/wedge.png" width="15%">

 * [Felippa's schemes](http://dx.doi.org/10.1108/02644400410554362) (6 schemes
   up to degree 6)

Example:
```python
val = quadpy.wedge.integrate(
    lambda x: numpy.exp(x[0]),
    [
      [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.7, 0.0],
      [0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [0.5, 0.7, 1.0],
    ],
    quadpy.wedge.Felippa(3)
    )
```

### Sphere
<img src="https://nschloe.github.io/quadpy/sphere.png" width="25%">

 * [Lebedev's schemes](https://en.wikipedia.org/wiki/Lebedev_quadpy) (32
   schemes up to degree 131)

Example:
```python
val = quadpy.sphere.integrate(
    lambda x: numpy.exp(x[0]),
    [0.0, 0.0, 0.0], 1.0,
    quadpy.sphere.Lebedev(19)
    )
```

### Installation

quadpy is [available from the Python Package Index](https://pypi.python.org/pypi/quadpy/), so with
```
pip install -U quadpy
```
you can install/upgrade.

### Testing

To run the tests, just check out this repository and type
```
MPLBACKEND=Agg pytest
```

### Distribution

To create a new release

1. bump the `__version__` number,

2. publish to PyPi and GitHub:
    ```
    $ make publish
    ```

### License
quadpy is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).