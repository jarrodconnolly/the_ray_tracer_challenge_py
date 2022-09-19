"""
Colour module
"""
from typing import Self
import math

class Colour:
  """
  Colours
  """
  def __init__(self, red: float, green: float, blue: float) -> Self:
    self.red = red
    self.green = green
    self.blue = blue

  def __eq__(self, other: Self):
    if isinstance(other, Colour):
      if(
        math.isclose(self.red, other.red, abs_tol=1e-05) and
        math.isclose(self.green, other.green, abs_tol=1e-05) and
        math.isclose(self.blue, other.blue, abs_tol=1e-05)
      ):
        return True
    return False

  def __add__(self, other: Self):
    return Colour(
      self.red + other.red,
      self.green + other.green,
      self.blue + other.blue)

  def __sub__(self, other: Self):
    return Colour(
      self.red - other.red,
      self.green - other.green,
      self.blue - other.blue)

  def __mul__(self, other: int|float|Self):
    if isinstance(other, Colour):
      return Colour(
        self.red * other.red,
        self.green * other.green,
        self.blue * other.blue)

    return Colour(
      self.red * other,
      self.green * other,
      self.blue * other)
