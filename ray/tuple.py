"""
Tuple module
"""
from __future__ import annotations
import math

class Tuple:
  """
  Tuple holds x y z w for points and vectors.
  """
  def __init__(self, x: float, y: float, z: float, w: int) -> Tuple:
    self.x = x
    self.y = y
    self.z = z
    self.w = w

  def __eq__(self, other: Tuple):
    if isinstance(other, Tuple):
      if(
        math.isclose(self.x, other.x, abs_tol=1e-05) and
        math.isclose(self.y, other.y, abs_tol=1e-05) and
        math.isclose(self.z, other.z, abs_tol=1e-05) and
        self.w == other.w
      ):
        return True
    return False

  def __add__(self, other: Tuple):
    return Tuple(
      self.x + other.x,
      self.y + other.y,
      self.z + other.z,
      self.w + other.w)

  def __sub__(self, other: Tuple):
    return Tuple(
      self.x - other.x,
      self.y - other.y,
      self.z - other.z,
      self.w - other.w)

  def __mul__(self, other: int|float):
    return Tuple(
      self.x * other,
      self.y * other,
      self.z * other,
      self.w * other)

  def __truediv__(self, other: int|float):
    return Tuple(
      self.x / other,
      self.y / other,
      self.z / other,
      self.w / other)

  def __neg__(self):
    return Tuple(-self.x, -self.y, -self.z, -self.w)

  def reflect(self, normal: Tuple) -> Tuple:
    """ return the vector refleced off the normal """
    return self - normal * 2 * self.dot(normal)

  def dot(self, tuple_b: Tuple) -> Tuple:
    """ Helper to compute the dot product """
    return (self.x * tuple_b.x) + (self.y * tuple_b.y) + (self.z * tuple_b.z) + (self.w * tuple_b.w)

  def cross(self, vector_b: Tuple) -> Tuple:
    """ Helper to compute cross product """
    return Vector(
      self.y * vector_b.z - self.z * vector_b.y,
      self.z * vector_b.x - self.x * vector_b.z,
      self.x * vector_b.y - self.y * vector_b.x)

  def magnitude(self) -> Tuple:
    """ return the magniture of the vector """
    return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2)

  def normalize(self) -> Tuple:
    """ return the normal of the vector """
    vector_magnitude = self.magnitude()
    return Tuple(
      self.x / vector_magnitude,
      self.y / vector_magnitude,
      self.z / vector_magnitude,
      self.w / vector_magnitude)

class Point(Tuple):
  """ Point specialization of Tuple """
  def __init__(self, x: float, y: float, z: float) -> Tuple:
    super().__init__(x, y, z, 1)

class Vector(Tuple):
  """ Vector specialization of Tuple """
  def __init__(self, x: float, y: float, z: float) -> Tuple:
    super().__init__(x, y, z, 0)
