"""
World module
"""
from __future__ import annotations
from rt.sphere import Sphere
from rt.shape import Shape
from rt.ray import Ray
from rt.tuple import Point
from rt.intersection import Intersections
from rt.light import PointLight
from rt.colour import Colour
from rt.material import Material
from rt.matrix import Matrix

class World:
  """
  World
  """
  def __init__(self) -> World:
    self.objects: list[Shape] = []
    self.lights = []

  def intersect(self, ray: Ray) -> Intersections:
    """ Intersect a ray with the world """
    intersections = Intersections()
    for o in self.objects:
      intersections.xs.extend(o.intersect(ray).xs)

    intersections.xs.sort(key=lambda i: i.t)

    return intersections

  @classmethod
  def DefaultWorld(cls) -> World:
    """ Return the default world """
    light = PointLight(Point(-10, 10, -10), Colour(1, 1, 1))

    s1 = Sphere(material=Material(
      colour=Colour(0.8, 1.0, 0.6),
      diffuse=0.7,
      specular=0.2))

    s2 = Sphere(transform=Matrix.scaling(0.5, 0.5, 0.5))

    w = World()
    w.objects.append(s1)
    w.objects.append(s2)
    w.lights.append(light)
    return w
