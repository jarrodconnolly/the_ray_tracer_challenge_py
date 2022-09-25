"""
World module
"""
from __future__ import annotations

from rt.colour import Colour
from rt.intersection import Comps, Intersection, Intersections
from rt.light import PointLight
from rt.material import Material
from rt.matrix import Matrix
from rt.ray import Ray
from rt.shape import Shape
from rt.sphere import Sphere
from rt.tuple import Point


class World:
  """
  World
  """
  def __init__(self) -> World:
    self.objects: list[Shape] = []
    self.lights: list[PointLight] = []

  def intersect(self, ray: Ray) -> Intersections:
    """ Intersect a ray with the world """
    intersections = Intersections()
    for o in self.objects:
      intersections.xs.extend(o.intersect(ray).xs)

    intersections.xs.sort(key=lambda i: i.t)

    return intersections

  def shade_hit(self, comps: Comps) -> Colour:
    """ shade function. get colour from all the lights """
    colour = Colour(0, 0, 0)
    shadowed = self.is_shadowed(comps.over_point)
    for light in self.lights:
      colour += comps.object.material.lighting(
      light,
      comps.point,
      comps.eyev,
      comps.normalv,
      shadowed)
    return colour

  def colour_at(self, ray: Ray) -> Colour:
    """ get colour from ray at world intersection """
    i = self.intersect(ray)
    hit: Intersection = i.hit()
    if hit is None:
      return Colour(0, 0, 0)
    comps = hit.prepare_computations(ray)
    return self.shade_hit(comps)

  def is_shadowed(self, p: Point) -> bool:
    """ is the point in shadow """
    v = self.lights[0].position - p
    distance = v.magnitude()
    direction = v.normalize()

    r = Ray(p, direction)
    intersections = self.intersect(r)

    h = intersections.hit()
    if h is not None and h.t < distance:
      return True
    return False

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
