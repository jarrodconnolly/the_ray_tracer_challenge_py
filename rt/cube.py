"""
Cube module
"""
from __future__ import annotations

import math

from rt.helpers import EPSILON
from rt.intersection import Intersection, Intersections
from rt.ray import Ray
from rt.shape import Shape
from rt.tuple import Point, Vector


class Cube(Shape):
  """
  Cube
  """
  def local_normal_at(self, local_point: Point) -> Vector:
    maxc = max(abs(local_point.x), abs(local_point.y), abs(local_point.z))
    if maxc == abs(local_point.x):
      return Vector(local_point.x, 0, 0)
    elif maxc == abs(local_point.y):
      return Vector(0, local_point.y, 0)
    return Vector(0, 0, local_point.z)

  def intersect(self, ray: Ray) -> Intersections:
    """ Compute intersections with ray """
    local_ray = super().intersect(ray)

    xtmin, xtmax = self.check_axis(local_ray.origin.x, local_ray.direction.x)
    ytmin, ytmax = self.check_axis(local_ray.origin.y, local_ray.direction.y)
    ztmin, ztmax = self.check_axis(local_ray.origin.z, local_ray.direction.z)
    tmin = max(xtmin, ytmin, ztmin)
    tmax = min(xtmax, ytmax, ztmax)

    if tmin > tmax:
      return Intersections()

    return Intersections(Intersection(tmin, self), Intersection(tmax, self))

  def check_axis(self, origin, direction):
    """ find min and max t values """
    tmin_numerator = (-1 - origin)
    tmax_numerator = (1 - origin)
    if abs(direction) >= EPSILON:
      tmin = tmin_numerator / direction
      tmax = tmax_numerator / direction
    else:
      tmin = tmin_numerator * float("inf")
      tmax = tmax_numerator * float("inf")

    if tmin > tmax:
      tmin, tmax = tmax, tmin
    return tmin, tmax
