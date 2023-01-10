"""
Cylinder module
"""
from __future__ import annotations

import math

from rt.helpers import EPSILON
from rt.intersection import Intersection, Intersections
from rt.ray import Ray
from rt.shape import Shape
from rt.tuple import Point, Vector


class Cylinder(Shape):
  """
  Cylinder
  """
  def local_normal_at(self, local_point: Point) -> Vector:
    return Vector(local_point.x, 0, local_point.z)

  def intersect(self, ray: Ray) -> Intersections:
    """ Compute intersections with ray """
    local_ray = super().intersect(ray)

    a = local_ray.direction.x ** 2 + local_ray.direction.z ** 2

    # ray is parallel to the y axis
    if math.isclose(a, 0, abs_tol=EPSILON):
      return Intersections()

    b = 2 * local_ray.origin.x * local_ray.direction.x + 2 * local_ray.origin.z * local_ray.direction.z
    c = local_ray.origin.x ** 2 + local_ray.origin.z ** 2 - 1

    disc = b ** 2 - 4 * a * c

    # ray does not intersect the cylinder
    if disc < 0:
      return Intersections()

    t0 = (-b - math.sqrt(disc)) / (2 * a)
    t1 = (-b + math.sqrt(disc)) / (2 * a)

    return Intersections(
      Intersection(t0, self),
      Intersection(t1, self)
    )
