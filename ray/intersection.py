"""
Intersection module
"""
from typing import Self

class Intersection:
  """
  Intersection
  """
  def __init__(self, distance: float, obj: object) -> Self:
    self.t = distance
    self.object = obj

class Intersections:
  """
  Intersections
  """
  def __init__(self, *intersections):
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

    visible = list(filter(lambda i: i.t >= 0, self.xs))
    if len(visible) == 0:
      return None

    return visible[0]
