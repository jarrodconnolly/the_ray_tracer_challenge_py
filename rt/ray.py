"""
Ray module
"""
from __future__ import annotations
import ray as Ray

class Ray:
  """
  Ray
  """
  def __init__(self, origin: Ray.Point, direction: Ray.Vector) -> Ray:
    self.origin: Ray.Point = origin
    self.direction: Ray.Vector = direction

  def position(self, distance: float) -> Ray.Point:
    """ Compute point some distance along ray """
    return self.origin + self.direction * distance

  def transform(self, transform: Ray.Matrix) -> Ray:
    """ Transform the ray """
    return Ray(transform * self.origin, transform * self.direction)
