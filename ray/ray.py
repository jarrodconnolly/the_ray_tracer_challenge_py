"""
Ray module
"""
from __future__ import annotations
from .tuple import Vector, Point
from .matrix import Matrix

class Ray:
  """
  Ray
  """
  def __init__(self, origin: Point, direction: Vector) -> Ray:
    self.origin = origin
    self.direction = direction

  def position(self, distance: float) -> Point:
    """ Compute point some distance along ray """
    return self.origin + self.direction * distance

  def transform(self, transform: Matrix) -> Ray:
    """ Transform the ray """
    return Ray(transform * self.origin, transform * self.direction)
