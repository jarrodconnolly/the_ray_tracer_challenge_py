"""
Intersection module
"""
from __future__ import annotations

import math

from rt.helpers import EPSILON
from rt.ray import Ray
from rt.shape import Shape
from rt.tuple import Point, Vector


class Comps:
  """ Prepared Computations """
  def __init__(self) -> Comps:
    self.t: int = None
    self.object: Shape
    self.point: Point
    self.eyev: Vector
    self.normalv: Vector
    self.inside: bool
    self.over_point: Point
    self.under_point: Point
    self.reflectv: Vector
    self.n1: float
    self.n2: float

  def schlick(self) -> float:
    """ Schlick approximation """
    # find the cosine of the angle between the eye and normal vectors
    cos = self.eyev.dot(self.normalv)

    # total internal reflection can only occur if n1 > n2
    if self.n1 > self.n2:
      n = self.n1 / self.n2
      sin2_t = n ** 2 * (1.0 - cos ** 2)
      if sin2_t > 1.0:
        return 1.0

      # compute cosine of theta_t using trig identity
      cos_t = math.sqrt(1.0 - sin2_t)

      # when n1 > n2, use cos(theta_t) instead
      cos = cos_t

    r0 = ((self.n1 - self.n2) / (self.n1 + self.n2)) ** 2
    return r0 + (1 - r0) * (1 - cos) ** 5

class Intersections:
  """
  Intersections
  """
  def __init__(self, *intersections) -> Intersections:
    self.xs = list(intersections)

  def __getitem__(self, key: int) -> Intersection:
    return self.xs[key]

  def __len__(self) -> int:
    return len(self.xs)

  def hit(self) -> Intersection|None:
    """ return the intersection that is the hit """
    if len(self.xs) == 0:
      return None

    self.xs.sort(key=lambda i: i.t)

    # visible = list(filter(lambda i: i.t >= 0, self.xs))
    visible = [i for i in self.xs if i.t >= 0]
    if len(visible) == 0:
      return None

    return visible[0]

class Intersection:
  """
  Intersection
  """
  def __init__(self, distance: float, obj: Shape) -> Intersection:
    self.t: int = distance
    self.object: Shape = obj

  def prepare_computations(self, ray: Ray, xs: Intersections = None) -> Comps:
    """ Prepare Computations """
    if xs is None:
      xs = Intersections(self)

    comps = Comps()
    comps.t = self.t
    comps.object = self.object
    comps.point = ray.position(comps.t)
    comps.eyev = -ray.direction
    comps.normalv = comps.object.normal_at(comps.point)

    if comps.normalv.dot(comps.eyev) < 0:
      comps.inside = True
      comps.normalv = -comps.normalv
    else:
      comps.inside = False

    comps.over_point = comps.point + comps.normalv * EPSILON
    comps.under_point = comps.point - comps.normalv * EPSILON
    comps.reflectv = ray.direction.reflect(comps.normalv)

    containers: list[Shape] = []
    for i in xs:
      if i == self:
        if len(containers) == 0:
          comps.n1 = 1.0
        else:
          comps.n1 = containers[-1].material.refractive_index

      if i.object in containers:
        containers.remove(i.object)
      else:
        containers.append(i.object)

      if i == self:
        if len(containers) == 0:
          comps.n2 = 1.0
        else:
          comps.n2 = containers[-1].material.refractive_index
        break

    return comps
