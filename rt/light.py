"""
Light module
"""
from __future__ import annotations
from rt.colour import Colour
from rt.tuple import Point

class PointLight:
  """
  PointLight
  """
  def __init__(self, position: Point, intensity: Colour) -> PointLight:
    self.position = position
    self.intensity = intensity

  def __eq__(self, o: PointLight) -> bool:
    return self.position == o.position and self.intensity == o.intensity
