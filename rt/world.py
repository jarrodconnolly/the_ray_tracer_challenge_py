"""
World module
"""
from __future__ import annotations

import math

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

  def refracted_colour(self, comps: Comps, remaining: int = 5) -> Colour:
    """ return the refracted colour """

    # stop at recursion limit
    if remaining <= 0:
      return Colour.Black()

    # not transparent
    if comps.object.material.transparency == 0:
      return Colour.Black()

    # total internal reflection (Snell’s Law)
    n_ratio = comps.n1 / comps.n2
    cos_i = comps.eyev.dot(comps.normalv)
    sin2_t = math.pow(n_ratio, 2) * (1 - math.pow(cos_i, 2))
    if sin2_t > 1:
      return Colour.Black()

    # find refract colour

    # Find cos(theta_t) via trigonometric identity
    cos_t = math.sqrt(1.0 - sin2_t)

    # Compute the direction of the refracted ray
    direction = comps.normalv * (n_ratio * cos_i - cos_t) - comps.eyev * n_ratio

    # Create the refracted ray
    refract_ray = Ray(comps.under_point, direction)

    # Find the color of the refracted ray, making sure to multiply
    # by the transparency value to account for any opacity
   #  next_remaining = remaining - 1
    colour = self.colour_at(refract_ray, remaining - 1) * comps.object.material.transparency

    # print(f"== remaining {remaining} ==")
    # print(f"n1: {comps.n1}")
    # print(f"n2: {comps.n2}")
    # print(f"eyev: {comps.eyev}")
    # print(f"normalv: {comps.normalv}")
    # print(f"under point: {comps.under_point}")
    # print(f"n_ratio: {n_ratio}")
    # print(f"cos_i: {cos_i}")
    # print(f"sin2_t: {sin2_t}")
    # print(f"cos_t: {cos_t}")
    # print(f"refract direction: {direction}")
    # print(f"refracted color: {colour}")
    # print("")

    return colour

  def reflected_colour(self, comps: Comps, remaining: int = 5) -> Colour:
    """ return the reflected colour """
    if remaining <= 0:
      return Colour.Black()

    if comps.object.material.reflective == 0:
      return Colour.Black()

    reflected_ray = Ray(comps.over_point, comps.reflectv)
    #next_remaining = remaining - 1
    colour = self.colour_at(reflected_ray, remaining - 1)

    return colour * comps.object.material.reflective

  def shade_hit(self, comps: Comps, remaining: int = 5) -> Colour:
    """ shade function. get colour from all the lights """
    shadowed = self.is_shadowed(comps.over_point)
    surface = comps.object.material.lighting(
      comps.object,
      self.lights[0],
      comps.over_point,
      comps.eyev,
      comps.normalv,
      shadowed)

    reflected = self.reflected_colour(comps, remaining)
    refracted = self.refracted_colour(comps, remaining)
    #return surface + reflected + refracted

    material = comps.object.material
    if material.reflective > 0 and material.transparency > 0:
      reflectance = comps.schlick()
      return surface + reflected * reflectance + refracted * (1 - reflectance)

    return surface + reflected + refracted


  def colour_at(self, ray: Ray, remaining: int = 5) -> Colour:
    """ get colour from ray at world intersection """
    xs = self.intersect(ray)
    hit: Intersection = xs.hit()
    if hit is None:
      return Colour(0, 0, 0)
    comps = hit.prepare_computations(ray, xs)
    return self.shade_hit(comps, remaining)

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
