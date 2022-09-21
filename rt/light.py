"""
Light module
"""
from __future__ import annotations
import rt as RT

class PointLight:
  """
  PointLight
  """
  def __init__(self, position: RT.Point, intensity: RT.Colour) -> PointLight:
    self.position = position
    self.intensity = intensity

  def __eq__(self, o: PointLight) -> bool:
    return self.position == o.position and self.intensity == o.intensity
