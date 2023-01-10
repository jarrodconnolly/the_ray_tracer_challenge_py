""" Cylinder Tests """
import math

from rt.cylinder import Cylinder
from rt.helpers import EPSILON
from rt.ray import Ray
from rt.tuple import Point, Vector


class TestCylinder:
  """ features/cylinders.feature """

  def test_cylinder_miss(self):
    """ A ray misses a cylinder """
    cyl = Cylinder()
    tests: list[tuple[Point, Vector]] = [
      (Point(1, 0, 0), Vector(0, 1, 0)),
      (Point(0, 0, 0), Vector(0, 1, 0)),
      (Point(0, 0, -5), Vector(1, 1, 1))
    ]

    for test in tests:
      direction = test[1].normalize()
      r = Ray(test[0], direction)
      xs = cyl.intersect(r)
      assert len(xs) == 0

  def test_cylinder_intersect(self):
    """ A ray strikes a cylinder """
    cyl = Cylinder()
    tests: list[tuple[Point, Vector, float, float]] = [
      (Point(1, 0, -5), Vector(0, 0, 1), 5, 5),
      (Point(0, 0, -5), Vector(0, 0, 1), 4, 6),
      (Point(0.5, 0, -5), Vector(0.1, 1, 1), 6.80798, 7.08872)
    ]

    for test in tests:
      direction = test[1].normalize()
      r = Ray(test[0], direction)
      xs = cyl.intersect(r)
      assert len(xs) == 2
      assert math.isclose(xs[0].t, test[2], abs_tol=EPSILON)
      assert math.isclose(xs[1].t, test[3], abs_tol=EPSILON)
