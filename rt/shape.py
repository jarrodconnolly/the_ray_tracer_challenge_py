"""
Shape module
"""
from __future__ import annotations

import abc

from rt.material import Material
from rt.matrix import Matrix
from rt.ray import Ray
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

  def intersect(self, ray: Ray):
    """ base class intersect """
    return ray.transform(self.transform.inverse)

  def normal_at(self, world_point: Point) -> Vector:
    """ return normal at a point """
    local_point: Point = self.transform.inverse * world_point
    local_normal: Vector = self.local_normal_at(local_point)
    world_normal: Vector = self.transform.inverse.transpose * local_normal
    world_normal.w = 0
    return world_normal.normalize()

  @abc.abstractmethod
  def local_normal_at(self, local_point: Point) -> Vector:
    """ return normal at a point """

class UnitTestShape(Shape):
  """ shape for unit tests """
  def __init__(self):
    self.saved_ray = None
    super().__init__()

  def local_normal_at(self, local_point) -> Vector:
    """ override for normal_at """
    return Vector(local_point.x, local_point.y, local_point.z)

  def intersect(self, ray: Ray):
    """ Compute intersections of ray with sphere """
    saved_ray = super().intersect(ray)
    self.saved_ray = saved_ray
  