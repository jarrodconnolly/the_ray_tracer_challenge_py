"""
Ray module
"""
from __future__ import annotations
import rt as RT

class Ray:
  """
  Ray
  """
  def __init__(self, origin: RT.Point, direction: RT.Vector) -> Ray:
    self.origin: RT.Point = origin
    self.direction: RT.Vector = direction

  def position(self, distance: float) -> RT.Point:
    """ Compute point some distance along ray """
    return self.origin + self.direction * distance

  def transform(self, transform: RT.Matrix) -> Ray:
    """ Transform the ray """
    return Ray(transform * self.origin, transform * self.direction)
