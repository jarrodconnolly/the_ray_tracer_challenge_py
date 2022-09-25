"""
Shape module
"""
from __future__ import annotations

import abc

from rt.material import Material
from rt.matrix import Matrix
from rt.tuple import Point, Vector


class Shape(metaclass=abc.ABCMeta):
  """ base class for shapes """
  def __init__(
    self,
    transform: Matrix = None,
    material: Material = None) -> Shape:
    if transform is None:
      transform = Matrix.identity()
    if material is None:
      material = Material()
    self.transform = transform
    self.material = material

  @abc.abstractmethod
  def normal_at(self, world_point: Point) -> Vector:
    """ return normal at a point """

class UnitTestShape(Shape):
  """ shape for unit tests """
  def normal_at(self, world_point) -> Vector:
    """ override for normal_at """
