"""
Intersection module
"""
from __future__ import annotations

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

class Intersection:
  """
  Intersection
  """
  def __init__(self, distance: float, obj: Shape) -> Intersection:
    self.t: int = distance
    self.object: Shape = obj

  def prepare_computations(self, ray: Ray) -> Comps:
    """ Prepare Computations """
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
    return comps

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
