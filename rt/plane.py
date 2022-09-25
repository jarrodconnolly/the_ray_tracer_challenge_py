"""
Plane module
"""
from __future__ import annotations

from rt.helpers import EPSILON
from rt.intersection import Intersection, Intersections
from rt.ray import Ray
from rt.shape import Shape
from rt.tuple import Point, Vector


class Plane(Shape):
  """
  Plane
  """

  def local_normal_at(self, local_point: Point) -> Vector:
    return Vector(0, 1, 0)

  def intersect(self, ray: Ray) -> Intersections:
    """ Compute intersections with ray """
    local_ray = super().intersect(ray)

    if abs(local_ray.direction.y) < EPSILON:
      return Intersections()

    t = -local_ray.origin.y / local_ray.direction.y
    return Intersections(Intersection(t, self))
