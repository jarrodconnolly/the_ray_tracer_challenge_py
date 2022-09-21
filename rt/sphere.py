"""
Sphere module
"""
from __future__ import annotations
import math
import ray as Ray

class Sphere:
  """
  Sphere
  """
  def __init__(
    self,
    transform: Ray.Matrix = Ray.Matrix.identity(),
    material: Ray.Material = Ray.Material()) -> Sphere:
    self.transform = transform
    self.material = material

  def __eq__(self, o: Sphere) -> bool:
    return self.transform == o.transform and self.material == o.material

  def intersect(self, ray: Ray) -> Ray.Intersections:
    """ Compute intersections of ray with sphere """
    transformed_ray = ray.transform(self.transform.inverse())

    sphere_to_ray = transformed_ray.origin - Ray.Point(0, 0, 0)

    a = transformed_ray.direction.dot(transformed_ray.direction)
    b = 2 * transformed_ray.direction.dot(sphere_to_ray)
    c = sphere_to_ray.dot(sphere_to_ray) - 1

    discriminant = b**2 - 4 * a * c

    if discriminant < 0:
      return Ray.Intersections()

    t1 = (-b - math.sqrt(discriminant)) / (2 * a)
    t2 = (-b + math.sqrt(discriminant)) / (2 * a)

    return Ray.Intersections(
      Ray.Intersection(t1, self),
      Ray.Intersection(t2, self)
    )

  def normal_at(self, world_point: Ray.Point) -> Ray.Vector:
    """ return normal at a point """
    object_point: Ray.Point = self.transform.inverse() * world_point
    object_normal: Ray.Vector = object_point - Ray.Point(0, 0, 0)
    world_normal: Ray.Vector = self.transform.inverse().transpose() * object_normal
    world_normal.w = 0
    return world_normal.normalize()
