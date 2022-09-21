"""
Ray module
"""
from __future__ import annotations
from rt.tuple import Point, Vector
from rt.matrix import Matrix

class Ray:
  """
  Ray
  """
  def __init__(self, origin: Point, direction: Vector) -> Ray:
    self.origin: Point = origin
    self.direction: Vector = direction

  def position(self, distance: float) -> Point:
    """ Compute point some distance along ray """
    return self.origin + self.direction * distance

  def transform(self, transform: Matrix) -> Ray:
    """ Transform the ray """
    return Ray(transform * self.origin, transform * self.direction)
