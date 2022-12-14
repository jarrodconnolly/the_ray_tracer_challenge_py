"""
Colour module
"""
from __future__ import annotations

import math

from rt.helpers import EPSILON


class Colour:
  """
  Colours
  """
  def __init__(self, red: float, green: float, blue: float) -> Colour:
    self.red = red
    self.green = green
    self.blue = blue

  def __eq__(self, other: Colour):
    if isinstance(other, Colour):
      if(
        math.isclose(self.red, other.red, abs_tol=EPSILON) and
        math.isclose(self.green, other.green, abs_tol=EPSILON) and
        math.isclose(self.blue, other.blue, abs_tol=EPSILON)
      ):
        return True
    return False

  def __str__(self) -> str:
    return f"v({round(self.red, 4):.4f},{round(self.green, 4):.4f},{round(self.blue, 4):.4f})"

  def __add__(self, other: Colour):
    return Colour(
      self.red + other.red,
      self.green + other.green,
      self.blue + other.blue)

  def __sub__(self, other: Colour):
    return Colour(
      self.red - other.red,
      self.green - other.green,
      self.blue - other.blue)

  def __mul__(self, other: int|float|Colour):
    if isinstance(other, Colour):
      return Colour(
        self.red * other.red,
        self.green * other.green,
        self.blue * other.blue)

    return Colour(
      self.red * other,
      self.green * other,
      self.blue * other)

  @classmethod
  def Black(cls):
    """ Black colour constant """
    return Colour(0, 0, 0)

  @classmethod
  def White(cls):
    """ White colour constant """
    return Colour(1, 1, 1)
