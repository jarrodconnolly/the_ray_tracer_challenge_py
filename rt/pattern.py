"""
Stripe module
"""
from __future__ import annotations

import abc
import math
from typing import TYPE_CHECKING

from rt.colour import Colour
from rt.matrix import Matrix

if TYPE_CHECKING:
  from rt.shape import Shape
  from rt.tuple import Point

class Pattern(metaclass=abc.ABCMeta):
  """ base class for patterns """
  def __init__(self, transform: Matrix = Matrix.identity()) -> Stripe:
    self.transform: Matrix = transform

  def pattern_at_shape(self, o: Shape, world_point:Point) -> Colour:
    """ get the colour using a shape and world point """
    object_point = o.transform.inverse * world_point
    pattern_point = self.transform.inverse * object_point
    return self.pattern_at(pattern_point)

  @abc.abstractmethod
  def pattern_at(self, p: Point) -> Colour:
    """ get the colour at a point """

class UnitTestPattern(Pattern):
  """ pattern for unit tests """
  def __init__(self) -> Stripe:
    super().__init__()
  def pattern_at(self, p: Point) -> Colour:
    """ get the colour at a point """
    return Colour(p.x, p.y, p.z)

class Stripe(Pattern):
  """
  Stripe
  """
  def __init__(self, a: Colour, b: Colour) -> Stripe:
    super().__init__()
    self.a = a
    self.b = b

  def pattern_at(self, p: Point) -> Colour:
    """ get the colour at a point """
    value = math.floor(p.x) % 2 == 0
    return self.a if value else self.b

class Gradient(Pattern):
  """ Gradient """
  def __init__(self, a: Colour, b: Colour) -> Gradient:
    super().__init__()
    self.a = a
    self.b = b

  def pattern_at(self, p: Point) -> Colour:
    """ get the colour at a point """
    distance = self.b - self.a
    fraction = p.x - math.floor(p.x)
    return self.a + distance * fraction

class Ring(Pattern):
  """ Ring """
  def __init__(self, a: Colour, b: Colour) -> Gradient:
    super().__init__()
    self.a = a
    self.b = b

  def pattern_at(self, p: Point) -> Colour:
    """ get the colour at a point """
    in_ring = math.floor(math.sqrt((p.x ** 2) + (p.z ** 2))) % 2 == 0
    if in_ring is True:
      return self.a
    return self.b

class Checker(Pattern):
  """ Checker """
  def __init__(self, a: Colour, b: Colour, uv_map = False) -> Gradient:
    super().__init__()
    self.a = a
    self.b = b
    self.uv_map = uv_map

  def pattern_at(self, p: Point) -> Colour:
    """ get the colour at a point """
    if self.uv_map is True:
      theta = math.atan2(p.x, p.z) + math.pi
      r = p.magnitude()
      phi = math.acos(p.y / r)
      u = theta / (2 * math.pi)
      v = phi / math.pi
      if (math.floor(u * 20) + math.floor(v * 10)) % 2 == 0:
        return self.a
      return self.b

    in_check = math.fmod(math.floor(p.x) + math.floor(p.y) + math.floor(p.z), 2)  == 0
    if in_check is True:
      return self.a
    return self.b
