"""
Sphere module
"""
from typing import Self
import math
from .ray import Ray
from .tuple import Point, Vector
from .intersection import Intersection, Intersections
from .matrix import Matrix
from .material import Material

class Sphere:
  """
  Sphere
  """
  def __init__(
    self,
    transform: Matrix = Matrix.identity(),
    material: Material = Material()) -> Self:
    self.transform = transform
    self.material = material

  def intersect(self, ray: Ray) -> Intersections:
    """ Compute intersections of ray with sphere """
    transformed_ray = ray.transform(self.transform.inverse())

    sphere_to_ray = transformed_ray.origin - Point(0, 0, 0)

    a = transformed_ray.direction.dot(transformed_ray.direction)
    b = 2 * transformed_ray.direction.dot(sphere_to_ray)
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

  def normal_at(self, world_point: Point) -> Vector:
    """ return normal at a point """
    object_point: Point = self.transform.inverse() * world_point
    object_normal: Vector = object_point - Point(0, 0, 0)
    world_normal: Vector = self.transform.inverse().transpose() * object_normal
    world_normal.w = 0
    return world_normal.normalize()
