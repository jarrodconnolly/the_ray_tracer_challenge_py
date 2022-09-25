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
