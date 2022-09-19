"""
Ray module
"""
from typing import Self
from .tuple import Vector, Point
from .matrix import Matrix

class Ray:
  """
  Ray
  """
  def __init__(self, origin: Point, direction: Vector) -> Self:
    self.origin = origin
    self.direction = direction

  def position(self, distance: float) -> Point:
    """ Compute point some distance along ray """
    return self.origin + self.direction * distance

  def transform(self, transform: Matrix) -> Self:
    """ Transform the ray """
    return Ray(transform * self.origin, transform * self.direction)
