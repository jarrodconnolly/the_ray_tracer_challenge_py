"""
Sphere module
"""
from __future__ import annotations

import math

from rt.intersection import Intersection, Intersections
# from rt.material import Material
# from rt.matrix import Matrix
from rt.ray import Ray
from rt.shape import Shape
from rt.tuple import Point, Vector


class Sphere(Shape):
  """
  Sphere
  """
  # def __init__(
  #   self,
  #   transform: Matrix = Matrix.identity(),
  #   material: Material = Material()) -> Sphere:
  #   super().__init__(transform, material)

  def __eq__(self, o: Sphere) -> bool:
    return self.transform == o.transform and self.material == o.material

  def intersect(self, ray: Ray) -> Intersections:
    """ Compute intersections of ray with sphere """
    local_ray = super().intersect(ray)

    sphere_to_ray = local_ray.origin - Point(0, 0, 0)

    a = local_ray.direction.dot(local_ray.direction)
    b = 2 * local_ray.direction.dot(sphere_to_ray)
    c = sphere_to_ray.dot(sphere_to_ray) - 1

    discriminant = b**2 - 4 * a * c

    if discriminant < 0:
      return Intersections()

    t1 = (-b - math.sqrt(discriminant)) / (2 * a)
    t2 = (-b + math.sqrt(discriminant)) / (2 * a)

    return Intersections(
      Intersection(t1, self),
      Intersection(t2, self)
    )

  def local_normal_at(self, local_point: Point) -> Vector:
    return local_point - Point(0, 0, 0)

  # def normal_at(self, world_point: Point) -> Vector:
  #   """ return normal at a point """
  #   object_point: Point = self.transform.inverse * world_point
  #   object_normal: Vector = object_point - Point(0, 0, 0)
  #   world_normal: Vector = self.transform.inverse.transpose * object_normal
  #   world_normal.w = 0
  #   return world_normal.normalize()
