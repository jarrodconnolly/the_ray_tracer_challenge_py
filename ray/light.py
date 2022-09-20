"""
Light module
"""
from __future__ import annotations
from .tuple import Point
from .colour import Colour

class PointLight:
  """
  PointLight
  """
  def __init__(self, position: Point, intensity: Colour) -> PointLight:
    self.position = position
    self.intensity = intensity
