"""
World module
"""
from __future__ import annotations
import ray as Ray

class World:
  """
  World
  """
  def __init__(self) -> World:
    self.objects: list[Ray.Sphere] = []
    self.lights = []

  def intersect(self, ray: Ray) -> Ray.Intersections:
    """ Intersect a ray with the world """
    intersections = Ray.Intersections()
    for o in self.objects:
      intersections.xs.extend(o.intersect(ray).xs)

    intersections.xs.sort(key=lambda i: i.t)

    return intersections

  @classmethod
  def DefaultWorld(cls) -> World:
    """ Return the default world """
    light = Ray.PointLight(Ray.Point(-10, 10, -10), Ray.Colour(1, 1, 1))

    s1 = Ray.Sphere(material=Ray.Material(
      colour=Ray.Colour(0.8, 1.0, 0.6),
      diffuse=0.7,
      specular=0.2))

    s2 = Ray.Sphere(transform=Ray.Matrix.scaling(0.5, 0.5, 0.5))

    w = World()
    w.objects.append(s1)
    w.objects.append(s2)
    w.lights.append(light)
    return w
