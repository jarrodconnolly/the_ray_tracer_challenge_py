"""
Sphere module
"""
from __future__ import annotations
import math
import rt as RT

class Sphere:
  """
  Sphere
  """
  def __init__(
    self,
    transform: RT.Matrix = RT.Matrix.identity(),
    material: RT.Material = RT.Material()) -> Sphere:
    self.transform = transform
    self.material = material

  def __eq__(self, o: Sphere) -> bool:
    return self.transform == o.transform and self.material == o.material

  def intersect(self, ray: RT.Ray) -> RT.Intersections:
    """ Compute intersections of ray with sphere """
    transformed_ray = ray.transform(self.transform.inverse())

    sphere_to_ray = transformed_ray.origin - RT.Point(0, 0, 0)

    a = transformed_ray.direction.dot(transformed_ray.direction)
    b = 2 * transformed_ray.direction.dot(sphere_to_ray)
    c = sphere_to_ray.dot(sphere_to_ray) - 1

    discriminant = b**2 - 4 * a * c

    if discriminant < 0:
      return RT.Intersections()

    t1 = (-b - math.sqrt(discriminant)) / (2 * a)
    t2 = (-b + math.sqrt(discriminant)) / (2 * a)

    return RT.Intersections(
      RT.Intersection(t1, self),
      RT.Intersection(t2, self)
    )

  def normal_at(self, world_point: RT.Point) -> RT.Vector:
    """ return normal at a point """
    object_point: RT.Point = self.transform.inverse() * world_point
    object_normal: RT.Vector = object_point - RT.Point(0, 0, 0)
    world_normal: RT.Vector = self.transform.inverse().transpose() * object_normal
    world_normal.w = 0
    return world_normal.normalize()
