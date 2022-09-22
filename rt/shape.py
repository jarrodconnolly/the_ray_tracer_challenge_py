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
    transform: Matrix = Matrix.identity(),
    material: Material = Material()) -> Shape:
    self.transform = transform
    self.material = material

  @abc.abstractmethod
  def normal_at(self, world_point: Point) -> Vector:
    """ return normal at a point """
