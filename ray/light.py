"""
Light module
"""
from typing import Self
from .tuple import Point
from .colour import Colour

class PointLight:
  """
  PointLight
  """
  def __init__(self, position: Point, intensity: Colour) -> Self:
    self.position = position
    self.intensity = intensity
