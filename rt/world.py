"""
World module
"""
from __future__ import annotations
import rt as RT

class World:
  """
  World
  """
  def __init__(self) -> World:
    self.objects: list[RT.Sphere] = []
    self.lights = []

  def intersect(self, ray: RT.Ray) -> RT.Intersections:
    """ Intersect a ray with the world """
    intersections = RT.Intersections()
    for o in self.objects:
      intersections.xs.extend(o.intersect(ray).xs)

    intersections.xs.sort(key=lambda i: i.t)

    return intersections

  @classmethod
  def DefaultWorld(cls) -> World:
    """ Return the default world """
    light = RT.PointLight(RT.Point(-10, 10, -10), RT.Colour(1, 1, 1))

    s1 = RT.Sphere(material=RT.Material(
      colour=RT.Colour(0.8, 1.0, 0.6),
      diffuse=0.7,
      specular=0.2))

    s2 = RT.Sphere(transform=RT.Matrix.scaling(0.5, 0.5, 0.5))

    w = World()
    w.objects.append(s1)
    w.objects.append(s2)
    w.lights.append(light)
    return w
